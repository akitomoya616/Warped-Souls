from abc import ABC, abstractmethod

class Observer(ABC):

    @abstractmethod
    def update(message, value):
        """An abstract observer interface for different observer classes to implement."""

class StatTracker(Observer):
    def __init__(self):
        self.stats = {}

    def update(self, message, value):
        if message in self.stats:
            self.stats[message] = self.stats[message] + value
        else:
            self.stats[message] = value

    def return_stats(self):
        return self.stats
