import abc


class IConfigsParser(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return hasattr(subclass, 'source_path') and \
                hasattr(subclass, 'backup_path') and \
                hasattr(subclass, 'backcopy_path') and \
                hasattr(subclass, 'options') and \
                hasattr(subclass, 'filetypes') and \
                hasattr(subclass, 'is_enabled') and \
                callable(subclass.is_enabled) and \
                hasattr(subclass, 'validate') and \
                callable(subclass.validate)