import typing
from os.path import isdir
from utils import OptionsFlag, FileTypeFlag
from iconfigsparser import IConfigsParser

class CLIConfigsParser(IConfigsParser):
    def __init__(self, args: typing.List[str]):
        self.args = args
        self.options = self.get_options(self.args)
        self.source_path = self.args[-2]
        self.backup_path = self.args[-1]
        self.backcopy_path = self.get_backcopy_path(self.options, self.args)

    @staticmethod
    def get_options(arguments: typing.List[str]) -> typing.List[OptionsFlag]:
        flags = OptionsFlag.NONE
        for option in arguments:
            flags |= OptionsFlag.from_string(option)
        return flags
    
    @staticmethod
    def get_backcopy_path(options: OptionsFlag, args: typing.List[str]):
        if not options & OptionsFlag.BACKCOPY_ENABLED:
            return None
        for i, arg in enumerate(args):
            if OptionsFlag.from_string(arg) & OptionsFlag.BACKCOPY_ENABLED:
                return args[i + 1]
        return None

    def validate(self):
        if isdir(self.source_path) and isdir(self.backup_path) and \
            (True if not self.is_enabled(OptionsFlag.BACKCOPY_ENABLED) else isdir(self.backcopy_path)):
            return True
        else:
            msg = "There was an error loading the configuration file.\n\nOne or more of the configured paths is invalid. Have you connected the external hard drive?"
            print("{}\n => Source: {}\n => Backup: {}{}".format(
                msg,
                self.source_path, 
                self.backup_path, 
                "\n => Backcopy: {}".format(self.backcopy_path) if self.is_enabled(OptionsFlag.BACKCOPY_ENABLED) else ""))
            return False
    
    def is_enabled(self, option: OptionsFlag) -> bool:
        return bool(option & self.options)
        