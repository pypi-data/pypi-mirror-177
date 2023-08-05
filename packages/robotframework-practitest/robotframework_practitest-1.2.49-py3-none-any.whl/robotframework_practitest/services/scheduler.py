import time
from abc import abstractmethod
from concurrent.futures import ThreadPoolExecutor
from enum import Enum
from queue import Queue, Empty
from threading import Thread, Event
from time import sleep
from typing import Callable

from robotframework_practitest.utils.logger import logger
from robotframework_practitest.utils import get_error_info
from robotframework_practitest.utils import singleton, thread_pool

DEFAULT_RETENTION_TIMEOUT = 300
PENDING_RETENTION_TIMEOUT = 60


class TaskType(Enum):
    Synchron = 'Synchron'
    Asynchron = 'Asynchron'
    Foreground = 'Foreground'


class CallableArgument(Callable):
    def __call__(self) -> str:
        raise NotImplementedError()


class Task:
    def __init__(self, callback: Callable, *args, **kwargs):
        self._callback = callback
        self._args = args
        self._kwargs = kwargs

    def __str__(self):
        return "{} ({}, {})".format(
            self._callback.__name__,
            ', '.join(f'{a}' for a in self._args),
            ', '.join([f'{k}={v}' for k, v in self._kwargs.items()])
        )

    def __call__(self):
        return self._callback(*self._args, **self._kwargs)

    def run(self, type_: TaskType):
        if type_ == TaskType.Foreground:
            return self()

        if type_ == TaskType.Asynchron:
            _BackgroundAsyncService(self.__class__.__name__).schedule_task(self)
        elif type_ == TaskType.Synchron:
            _BackgroundSyncService(self.__class__.__name__).schedule_task(self)
        else:
            raise TypeError(f"Task '{self}' have unknown type")

    @staticmethod
    def shutdown(timeout=DEFAULT_RETENTION_TIMEOUT, callback: Callable = None, *args, **kwargs):
        _BackgroundSyncService().join(timeout, callback, *args, **kwargs)
        _BackgroundAsyncService().join(timeout, callback, *args, **kwargs)


class _BackGroundAbstract:
    def __init__(self, name=None):
        self.name = name or self.__class__.__name__

    @abstractmethod
    def schedule_task(self, task: Task):
        pass

    def join(self, timeout=DEFAULT_RETENTION_TIMEOUT, callback: Callable = None, *args, **kwargs):
        pass


@singleton.Singleton
class _BackgroundSyncService(_BackGroundAbstract):
    def __init__(self, name=None, maxsize=0, thread_interval=0.2):
        self._event = Event()
        self._active = Event()
        self._queue = Queue(maxsize)
        self._thread_interval = thread_interval
        name = name or self.__class__.__name__
        _BackGroundAbstract.__init__(self, "Sync " + name)
        self._thread = Thread(target=self._worker, name=self.name, daemon=False)
        # logger.register_thread_to_logger(self.name)
        logger.info(f"Starting {self.name}...")
        self._thread.start()

    def _worker(self):
        logger.info(f"{self.__class__.__name__}::_worker started")
        while not self._event.is_set():
            try:
                task_obj = self._queue.get()
                logger.debug(f"{self.__class__.__name__}::Task '{task_obj}' start")
                task_obj()
                logger.debug(f"{self.__class__.__name__}::Task '{task_obj}' done")
            except Empty:
                pass
            except Exception as e:
                f, li = get_error_info()
                logger.info(f"Error: {e}; File: {f}:{li}")
            finally:
                sleep(self._thread_interval)
        logger.info(f"{self.__class__.__name__}::_worker ended")

    def schedule_task(self, item: Task):
        if not self._active.is_set():
            self._queue.put(item)
            logger.debug(f"Task '{item}' added")
        else:
            logger.warning("Service ending awaiting; New task adding not possible now")

    def join(self, timeout=None, callback: Callable = None, *args, **kwargs):
        timeout = timeout or DEFAULT_RETENTION_TIMEOUT
        logger.debug(f'Join; Remains {self._queue.qsize()} tasks')
        self._active.set()
        start_ts = time.perf_counter()
        display_ts = time.perf_counter()
        while True:
            try:
                assert not self._queue.empty()
                if (time.perf_counter() - start_ts) >= timeout:
                    raise TimeoutError(f"Test completion taking too much time - {timeout}")
                if (time.perf_counter() - display_ts) >= PENDING_RETENTION_TIMEOUT:
                    logger.info("\nPractiTest reporter: Tests not completed yet:{}".format(
                        f"\n{callback(*args, **kwargs)}" if callback else ""
                    ))
                    display_ts = time.perf_counter()
                sleep(1)
            except AssertionError:
                logger.info("All tests completed:{}".format(
                    f"\n{callback(*args, **kwargs)}" if callback else ""
                ))
                break
            except TimeoutError as e:
                logger.error("PractiTest reporter: {}\nTests not completed yet:{}\n".format(
                    e,
                    f"\n{callback(*args, **kwargs)}" if callback else ""
                ))
                raise
            except Exception as e:
                f, li = get_error_info()
                logger.error(f"{type(e).__name__}: {e}; File: {f}:{li}")
                raise

        logger.debug(f'All tasks completed')
        self._event.set()
        logger.info(f"Stopped {self.name}.")


@singleton.Singleton
class _BackgroundAsyncService(_BackGroundAbstract):
    def __init__(self, name=None):
        name = name or self.__class__.__name__
        super().__init__("Async " + name)
        self.executor = thread_pool.MeasuredThreadPool(thread_name_prefix=self.name)
        self.active = True

    def schedule_task(self, task: Task):
        if not self.active:
            logger.warning("Service ending awaiting; New task adding not possible now")
            return
        self.executor.submit(task)

    def join(self, timeout=DEFAULT_RETENTION_TIMEOUT, callback: Callable = None, *args, **kwargs):
        logger.debug(f'Join; Remains {self.executor.size} tasks')
        self.executor.shutdown(wait=True)
        logger.info(f"Stopped {self.name}...")


def run_task(task_type: TaskType, callback: Callable, *args, **kwargs):
    Task(callback, *args, **kwargs).run(task_type)


__all__ = [
    'TaskType',
    'Task',
    'run_task'
]
