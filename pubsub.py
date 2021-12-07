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
        """Prints the given message
        Note: be careful when using TKinter objects, they have an update function"""
        print(message)

class ChannelPublisher():
    """Variant of Publisher that has different channels"""
    def __init__(self):
        self._channels = {}
        
    def add_channel(self, channel):
        """Sugar syntax to create a new, empty channel"""
        self._channels[channel] = self.Channel()
        
    def get_channel(self, channel):
        return self._channels[channel]
        
    def add_subscriber(self, channel, subscriber):
        assert isinstance(subscriber, Subscriber)
        self._channels[channel].add_subscriber(subscriber)

    def remove_subscriber(self, channel=None, subscriber=None):
        if channel is None:
            self._channels.clear()
        else:
            self._channels[channel].remove_subscriber(subscriber)

    def publish(self, channel, message):
        self._channels[channel].publish(message)
            
    def get_last(self, channel):
        return self._channels[channel].get_last()
    
    class Channel(Publisher, Subscriber):
        def __init__(self):
            self._last = None
            
            # Initialize Publisher
            Publisher.__init__(self)
            
            # Initialize Subscriber
            Subscriber.__init__(self)
        
        def get_last(self):
            """Gets the last message sent on the channel.
            Example usage: a widget needs to display the current Pokemon. When the
            widget is created use this to get the current Pokemon, then subscribe
            to make sure it stays up to date"""
            return self._last
        
        def publish(self, message):
            super().publish(message)
            self._last = message
        
        def update(self, message):
            """Pass the message along"""
            self.publish(message)

class Observer(Subscriber):
    def __init__(self, subject):
        super().__init__()
        assert isinstance(subject, Observable)
        self.subject = subject
        subject.add_subscriber(self)
        
    def update(self, message):
        """Should be implemented in inheriting classes to fetch the appropriate
        information from the subject
        Note: be careful when using TKinter objects, they have an update function"""
        raise NotImplementedError()
    
class Observable(Publisher):
    """
    Instead of publishing a message, the Publish function just serves to alert
    subscribers that a change has happened
    """
    def __init__(self):
        super().__init__()
