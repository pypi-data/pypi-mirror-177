from concurrent.futures import ThreadPoolExecutor


class MeasuredThreadPool(ThreadPoolExecutor):
    def __init__(self, max_workers=None, thread_name_prefix='', initializer=None, initargs=()):
        super().__init__(max_workers, thread_name_prefix, initializer, initargs)

    @property
    def size(self):
        return self._work_queue.qsize()
