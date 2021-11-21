class Publisher:
    def __init__(self):
        self._subs = []
        
    def add_subscriber(self, subscriber):
        assert isinstance(subscriber, Subscriber)
        self._subs.append(subscriber)

    def remove_subscriber(self, subscriber=None):
        if subscriber is None:
            self._subs.clear()
        else:
            self._subs.remove(subscriber)

    def publish(self, message):
        for sub in self._subs:
            sub.update(message)


class Subscriber:
    def update(self, message):
        print(message)
