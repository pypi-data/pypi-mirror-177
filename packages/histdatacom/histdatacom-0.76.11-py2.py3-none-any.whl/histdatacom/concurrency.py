import sys
from math import ceil
from multiprocessing import Process
from multiprocessing import managers
from multiprocessing import cpu_count
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import ProcessPoolExecutor
from concurrent.futures import as_completed
from influxdb_client import InfluxDBClient
from influxdb_client import WriteOptions
from influxdb_client import WritePrecision
from influxdb_client.client.write_api import WriteType
from rich.progress import Progress
from rich.progress import TextColumn
from rich.progress import BarColumn
from rich.progress import TimeElapsedColumn
from histdatacom.records import Records
from histdatacom import config
from typing import Callable

def init_counters(records_current_, records_next_, args_, csv_chunks_queue_=None):
    global records_current
    records_current = records_current_
    global records_next
    records_next = records_next_
    global args
    args = args_

    if csv_chunks_queue_ != None:
        global csv_chunks_queue
        csv_chunks_queue = csv_chunks_queue_

def complete_future(progress, task_id, futures, future):
    progress.advance(task_id, 0.75)
    futures.remove(future)
    del future

class ThreadPool():
    def __init__(self, exec_func,
                 args,
                 progress_pre_text, progress_post_text, cpu_count):

        self.exec_func = exec_func
        self.args = args
        self.progress_pre_text = progress_pre_text
        self.progress_post_text = progress_post_text
        self.cpu_count = cpu_count


    def __call__(self, records_current, records_next):

        records_count = records_current.qsize()
        with Progress(TextColumn(text_format=f"[cyan]{self.progress_pre_text} {records_count} {self.progress_post_text}."),
                      BarColumn(),
                      "[progress.percentage]{task.percentage:>3.0f}%",
                      TimeElapsedColumn()) as progress:
            task_id = progress.add_task("Validating URLs", total=records_count)

            with ThreadPoolExecutor(max_workers=self.cpu_count,
                                    initializer=init_counters,
                                    initargs=(records_current,
                                              records_next,
                                              self.args.copy())) as executor:
                futures = []

                while not records_current.empty():
                    record = records_current.get()

                    if record is None:
                        return

                    future = executor.submit(self.exec_func, record, self.args)
                    progress.advance(task_id, 0.25)
                    futures.append(future)

                for future in as_completed(futures):
                    complete_future(progress, task_id, futures, future)

        records_current.join()
        records_next.dump_to_queue(records_current)

class ProcessPool():
    def __init__(self, exec_func: Callable,
                 args: dict,
                 progress_pre_text: str, progress_post_text: str,
                 cpu_count: int,
                 join: bool=True,
                 dump: bool=True) -> None:

        self.exec_func = exec_func
        self.args = args
        self.progress_pre_text = progress_pre_text
        self.progress_post_text = progress_post_text
        self.cpu_count = cpu_count
        self.join = join
        self.dump = dump


    def __call__(self, records_current: Records,
                       records_next: Records,
                       csv_chunks_queue: Records=None) -> None:

        records_count = records_current.qsize()
        with Progress(TextColumn(text_format=f"[cyan]{self.progress_pre_text} {records_count} {self.progress_post_text}."),
                      BarColumn(),
                      "[progress.percentage]{task.percentage:>3.0f}%",
                      TimeElapsedColumn()) as progress:
            task_id = progress.add_task("Validating URLs", total=records_count)

            with ProcessPoolExecutor(max_workers=self.cpu_count,
                                    initializer=init_counters,
                                    initargs=(records_current,
                                              records_next,
                                              self.args.copy(),
                                              csv_chunks_queue)) as executor:
                futures = []

                while not records_current.empty():
                    record = records_current.get()

                    if record is None:
                        return

                    if csv_chunks_queue is None:
                        future = executor.submit(self.exec_func,
                                                 record,
                                                 self.args,
                                                 records_current,
                                                 records_next)
                    else:
                        future = executor.submit(self.exec_func,
                                                 record,
                                                 self.args,
                                                 records_current,
                                                 records_next,
                                                 csv_chunks_queue)

                    progress.advance(task_id, 0.25)
                    futures.append(future)

                for future in as_completed(futures):
                    complete_future(progress, task_id, futures, future)

        if self.join:
            records_current.join()

        if self.dump:
            records_next.dump_to_queue(records_current)

def get_pool_cpu_count(count: str | int | None=None) -> int:

    try:
        real_vcpu_count = cpu_count()

        if count is None:
            count = real_vcpu_count
        else:
            err_text_cpu_level_err = \
            f"""
                    ERROR on -c {count}  ERROR
                        * Malformed command:
                            - -c cpu must be str: low, medium, or high. or integer percent 1-200
            """
            count = str(count)
            match count:
                case "low":
                    count = ceil(real_vcpu_count / 2.5)
                case "medium":
                    count = ceil(real_vcpu_count / 1.5)
                case "high":
                    count = real_vcpu_count
                case _:
                    if count.isnumeric() and 1 <= int(count) <= 200:
                        count =  ceil(real_vcpu_count * (int(count) / 100))
                    else:
                        raise ValueError(err_text_cpu_level_err)

        return count - 1 if count > 2 else ceil(count / 2)
    except ValueError as err:
        print(err)
        sys.exit(err)

class QueueManager():
    def __init__(self, options):
        self.options = options
        self.records_manager=managers.SyncManager()
        self.records_manager.register("Records", Records)

    def __call__(self, runner_):
        self.records_manager.start()

        config.current_queue = self.records_manager.Records()
        config.next_queue = self.records_manager.Records()
        config.csv_chunks_queue = self.records_manager.Queue()

        histdatacom_runner = runner_(self.options)

        if self.options.from_api:
            return histdatacom_runner.run()
        else:
            histdatacom_runner.run()

class InfluxDBWriter(Process):
    def __init__(self, args, csv_chunks_queue):
        Process.__init__(self)
        self.args = args
        self.csv_chunks_queue = csv_chunks_queue
        self.client = InfluxDBClient(url=self.args['INFLUX_URL'],
                                     token=self.args['INFLUX_TOKEN'],
                                     org=self.args['INFLUX_ORG'],
                                     debug=False)
        self.write_api = self.client.write_api(write_options=WriteOptions(
                                               write_type=WriteType.batching,
                                               batch_size=25_000,
                                               flush_interval=12_000))

    def run(self):
        while True:
            chunk = self.csv_chunks_queue.get()

            if chunk is None:
                self.terminate()
                self.csv_chunks_queue.task_done()
                break

            self.write_api.write(org=self.args['INFLUX_ORG'],
                                 bucket=self.args['INFLUX_BUCKET'],
                                 record=chunk,
                                 write_precision=WritePrecision.MS)
            self.csv_chunks_queue.task_done()

    def terminate(self):
        self.write_api.__del__()
        self.client.__del__()
