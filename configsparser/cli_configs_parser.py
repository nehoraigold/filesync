import typing
from os.path import isdir
from utils.utils import OptionsFlag, FileTypeFlag
from configsparser.iconfigsparser import IConfigsParser


class CLIConfigsParser(IConfigsParser):
    def __init__(self, args: typing.List[str]):
        self.args = args
        self.options = self.get_options()
        self.filetypes = self.get_filetypes() if not self.is_enabled(OptionsFlag.HELP) else None
        self.source_path = self.args[-2] if not self.is_enabled(OptionsFlag.HELP) else None
        self.backup_path = self.args[-1] if not self.is_enabled(OptionsFlag.HELP) else None
        self.backcopy_path = self.get_backcopy_path() if not self.is_enabled(OptionsFlag.HELP) else None

    def get_options(self) -> OptionsFlag:
        flags = OptionsFlag.NONE
        for option in self.args:
            flags |= OptionsFlag.from_string(option)
        return flags

    def get_filetypes(self) -> FileTypeFlag:
        if not self.is_enabled(OptionsFlag.SPECIFIC_FILETYPE):
            return FileTypeFlag.ALL_TYPE
        filetypes = FileTypeFlag.NONE
        flag_found = False
        for arg in self.args:
            if flag_found:
                new_filetype = FileTypeFlag.from_string(arg)
                if not new_filetype:
                    break
                filetypes |= new_filetype
                continue
            if OptionsFlag.from_string(arg) & OptionsFlag.SPECIFIC_FILETYPE:
                flag_found = True
        return filetypes

    def get_backcopy_path(self):
        if not self.is_enabled(OptionsFlag.BACKCOPY_ENABLED):
            return None
        for i, arg in enumerate(self.args):
            if OptionsFlag.from_string(arg) & OptionsFlag.BACKCOPY_ENABLED:
                return self.args[i + 1]
        return None

    def validate(self):
        if isdir(self.source_path) and isdir(self.backup_path) and \
                (True if not self.is_enabled(OptionsFlag.BACKCOPY_ENABLED) else isdir(self.backcopy_path)):
            return True
        else:
            msg = "There was an error loading the configuration file.\n\nOne or more of the configured paths is " \
                  "invalid. Have you connected the external hard drive? "
            print("{}\n => Source: {}\n => Backup: {}{}".format(
                msg,
                self.source_path,
                self.backup_path,
                "\n => Backcopy: {}".format(self.backcopy_path) if self.is_enabled(
                    OptionsFlag.BACKCOPY_ENABLED) else ""))
            return False

    def is_enabled(self, option: OptionsFlag) -> bool:
        return bool(option & self.options)
