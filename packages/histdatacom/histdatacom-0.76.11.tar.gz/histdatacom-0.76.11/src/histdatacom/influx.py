import os
import sys
import io
import pytz
import yaml
from datetime import datetime

import rx
from rx import operators as ops

from concurrent.futures import ProcessPoolExecutor

from urllib.request import urlopen
from csv import DictReader

from functools import partial
from collections import namedtuple

from rich import print
from rich.progress import Progress
from rich.progress import TextColumn, TimeElapsedColumn, SpinnerColumn

from histdatacom.fx_enums import TimeFormat
from histdatacom.utils import get_csv_dialect
from histdatacom.concurrency import get_pool_cpu_count
from histdatacom.concurrency import ProcessPool
from histdatacom.concurrency import InfluxDBWriter
from histdatacom.api import _API
from histdatacom import config

class _Influx():
    def init_counters(self, csv_chunks_queue_, records_current_, records_next_, args_):
        global csv_chunks_queue
        csv_chunks_queue = csv_chunks_queue_
        global records_current
        records_current = records_current_
        global records_next
        records_next = records_next_
        global args
        args = args_

    def parse_csv_row(self, row, record):
        # line protocol example: myMeasurement,tag1=value1,tag2=value2 fieldKey="fieldValue" 1556813561098000000
        measurement = f"{record.data_fxpair}"
        tags = f"source=histdata.com,format={record.data_format},timeframe={record.data_timeframe}".replace(" ", "")
        time = self.convert_datetime_to_utc_timestamp(record.data_format,
                                                      record.data_timeframe,
                                                      row)

        match record.data_timeframe:
            case "M1":
                fields = f"openbid={row['openBid']},highbid={row['highBid']},lowbid={row['lowBid']},closebid={row['closeBid']}".replace(" ", "")
            case "T":
                fields = f"bidquote={row['bidQuote']},askquote={row['askQuote']}".replace(" ", "")

        line_protocol = f"{measurement},{tags} {fields} {time}"

        return line_protocol

    def parse_csv_rows(self, rows, record):
        mapfunc = partial(self.parse_csv_row, record=record)
        _parsed_rows = list(map(mapfunc, rows))

        csv_chunks_queue.put(_parsed_rows)

    def parse_jay_row(self, row, record):
        measurement = f"{record.data_fxpair}"
        tags = f"source=histdata.com,format={record.data_format},timeframe={record.data_timeframe}".replace(" ", "")

        match record.data_timeframe:
            case "M1":
                _row = namedtuple('_row', ['datetime', 'open', 'high', 'low', 'close', 'vol'])
                named_row = _row(row[0], row[1], row[2], row[3], row[4], row[5])

                fields = f"openbid={named_row.open},highbid={named_row.high},lowbid={named_row.low},closebid={named_row.close}".replace(" ", "")
                time = str(named_row.datetime)
            case "T":
                _row = namedtuple('_row', ['datetime','bid','ask','vol'])
                named_row = _row(row[0], row[1], row[2], row[3])

                fields = f"bidquote={named_row.bid},askquote={named_row.ask}".replace(" ", "")
                time = str(named_row.datetime)

        line_protocol = f"{measurement},{tags} {fields} {time}"

        return line_protocol

    def parse_jay_rows(self, iterable, record):
        mapfunc = partial(self.parse_jay_row, record=record)
        _parsed_rows = list(map(mapfunc, iterable))

        csv_chunks_queue.put(_parsed_rows)

    def import_file(self, record, args, records_current, records_next, csv_chunks_queue):
        try:
            if str.lower(record.data_format) == "ascii":
                jay_path = f"{record.data_dir}.data"
                if os.path.exists(jay_path):
                    self.import_jay(record, args, records_current, records_next, csv_chunks_queue)
                elif "CSV" in record.status:
                    if "ZIP" in record.status:
                        _API.test_for_jay_or_create(record, args)
                        self.import_jay(record, args,
                                        records_current, records_next,
                                        csv_chunks_queue)
                    else:
                        self.import_csv(record, args,
                                        records_current, records_next,
                                        csv_chunks_queue)

            records_next.put(record)
        except Exception:
            print("Unexpected error from here:", sys.exc_info())
            record.delete_into_file()
            raise
        finally:
            records_current.task_done()

    def import_jay(self, record, args, records_current, records_next, csv_chunks_queue):

        jay = _API.import_jay_data(record.data_dir + record.jay_filename)

        with ProcessPoolExecutor(max_workers=2,
                                 initializer=self.init_counters,
                                 initargs=(csv_chunks_queue,
                                           records_current,
                                           records_next,
                                           config.args)) as executor:

            data = rx.from_iterable(jay.to_tuples()) \
                .pipe(ops.buffer_with_count(25_000),
                      ops.flat_map(
                        lambda rows: executor.submit(self.parse_jay_rows, rows, record)))

            data.subscribe(
                on_next=lambda x: None,
                on_error=lambda er: print(f"Unexpected error: {er}"))

        record.status = "INFLUX_UPLOAD"
        record.write_info_file(base_dir=args['default_download_dir'])

    def import_csv(self, record, args, records_current, records_next, csv_chunks_queue):
        csv_path = record.data_dir + record.csv_filename
        file_endpoint = f"file://{record.data_dir}{record.csv_filename}"

        res = urlopen(file_endpoint)
        io_wrapper = io.TextIOWrapper(res)

        with ProcessPoolExecutor(max_workers=2,
                                 initializer=self.init_counters,
                                 initargs=(csv_chunks_queue,
                                           records_current,
                                           records_next,
                                           config.args)) as executor:

            fieldnames = self.fieldnames_match(record.data_format, record.data_timeframe)
            dialect = get_csv_dialect(csv_path)
            data = rx.from_iterable(
                DictReader(io_wrapper,
                           fieldnames=fieldnames,
                           dialect=dialect)) \
                .pipe(
                    ops.buffer_with_count(25_000),
                    ops.flat_map(
                        lambda rows: executor.submit(self.parse_csv_rows, rows, record)))

            data.subscribe(
                on_next=lambda x: None,
                on_error=lambda er: print(f"Unexpected error: {er}"))

        os.remove(csv_path)
        record.status = "INFLUX_UPLOAD"
        record.write_info_file(base_dir=args['default_download_dir'])

    def import_data(self):

        writer = InfluxDBWriter(config.args, config.csv_chunks_queue)
        writer.start()

        pool = ProcessPool(self.import_file,
                           config.args,
                           "Adding", "CSVs to influx queue...",
                           get_pool_cpu_count(config.args['cpu_utilization']) - 1\
                                              if get_pool_cpu_count(config.args['cpu_utilization']) >= 2 \
                                              else 1,
                           join=False,
                           dump=False)

        pool(config.current_queue, config.next_queue, config.csv_chunks_queue)

        with Progress(TextColumn(text_format="[cyan]...finishing upload to influxdb"),
                      SpinnerColumn(), SpinnerColumn(), SpinnerColumn(),
                      TimeElapsedColumn()) as progress:
            task_id = progress.add_task("waiting", total=0)

            config.current_queue.join()
            config.csv_chunks_queue.put(None)
            config.csv_chunks_queue.join()
            progress.advance(task_id, 0.75)

        print("[cyan] done.")
        config.next_queue.dump_to_queue(config.current_queue)

    @classmethod
    def load_influx_yaml(cls):

        if os.path.exists('influxdb.yaml'):
            with open('influxdb.yaml', 'r') as file:
                try:
                    yamlfile = yaml.safe_load(file)
                except yaml.YAMLError as exc:
                    print(exc)
                    sys.exit()

            return yamlfile

        print(""" ERROR: -I flag is used to import data to a influxdb instance...
                          there is no influxdb.yaml file in working directory.
                          did you forget to set it up?
              """)
        sys.exit()

    @classmethod
    def fieldnames_match(cls, csv_format, timeframe):
        try:
            match csv_format:
                case "ASCII" if timeframe == "M1":
                    fieldnames = ["msSinceEpochUTC", "openBid", "highBid", "lowBid", "closeBid", "Volume"]
                case "ASCII" if timeframe == "T":
                    fieldnames = ["msSinceEpochUTC", "bidQuote", "askQuote", "Volume"]
                case _:
                    raise ValueError("Invalid format for influx import")
            return fieldnames
        except ValueError as err:
            print(err)
            sys.exit()

    @classmethod
    def get_timeformat(cls, csv_format, timeframe):

        format_enum_key = f'{str(csv_format)}_{str(timeframe)}'

        return TimeFormat[format_enum_key].value

    @classmethod
    def convert_datetime_to_utc_timestamp(cls, csv_format, timeframe, row):

        est_timestamp = row["msSinceEpochUTC"]
        date_object = datetime.strptime(est_timestamp, cls.get_timeformat(csv_format, timeframe))
        tz_date_object = date_object.replace(tzinfo=pytz.timezone("Etc/GMT-5"))

        timestamp = int(tz_date_object.timestamp() * 1000)

        return str(timestamp)
