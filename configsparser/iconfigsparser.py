from abc import ABCMeta, abstractmethod
from utils.utils import OptionsFlag


class IConfigsParser(metaclass=ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return hasattr(subclass, 'source_path') and \
                hasattr(subclass, 'backup_path') and \
                hasattr(subclass, 'backcopy_path') and \
                hasattr(subclass, 'options') and \
                hasattr(subclass, 'filetypes')

    @abstractmethod
    def is_enabled(self, option_flag: OptionsFlag) -> bool:
        raise NotImplementedError

    @abstractmethod
    def validate(self) -> bool:
        raise NotImplementedError
