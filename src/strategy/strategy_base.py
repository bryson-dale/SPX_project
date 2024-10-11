# strategy/strategy_base.py

from abc import ABC, abstractmethod

class Strategy(ABC):
    @abstractmethod
    def set_parameters(self, **kwargs):
        pass

    @abstractmethod
    def generate_signals(self):
        pass