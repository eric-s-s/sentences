
from abc import ABC, abstractmethod


class AbstractWord(ABC):

    @property
    @abstractmethod
    def value(self) -> str:
        pass

    @abstractmethod
    def capitalize(self) -> 'AbstractWord':
        pass

    @abstractmethod
    def de_capitalize(self) -> 'AbstractWord':
        pass

    @abstractmethod
    def bold(self) -> 'AbstractWord':
        pass

    @abstractmethod
    def has_tags(self, *tags) -> bool:
        pass
