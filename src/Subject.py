from abc import ABC, abstractmethod

class Subject(ABC):

    @abstractmethod
    def registerObserver(self, o):
        """Allows a subject to register an Observer."""
    
    @abstractmethod
    def removeObserver(self, o):
        """Allows a subject to remove an Observer."""

    @abstractmethod
    def notifyObservers(self, message, value):
        """All registered/subscribed Observers will handle new information published by the Subject."""

