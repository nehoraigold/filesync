from abc import ABCMeta, abstractmethod


class ICopier(metaclass=ABCMeta):
    @abstractmethod
    def copy(self) -> int:
        raise NotImplementedError
