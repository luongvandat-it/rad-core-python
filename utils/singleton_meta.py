from threading import Lock


class SingletonMeta(type):
    _instance = None
    _lock = Lock()

    def __call__(self, *args, **kwargs):
        with self._lock:
            if not self._instance:
                self._instance = super().__call__(*args, **kwargs)
        return self._instance
