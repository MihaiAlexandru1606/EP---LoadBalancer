from threading import Lock


class AtomicInt(object):

    def __init__(self, value):
        self.values = value
        self.lock = Lock()

    def get_values(self):
        return self.values

    def decrement_values(self):
        with self.lock:
            self.values -= 1
