class Publisher:
    def add_subscriber(self, subscriber):
        raise NotImplementedError

    def remove_subscriber(self):
        raise NotImplementedError

    def publish(self, message):
        raise NotImplementedError


class Subscriber:
    def update(self, message):
        print(message)
