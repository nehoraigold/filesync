import json
from configsparser.iconfigsparser import IConfigsParser
from utils.utils import OptionsFlag, FileTypeFlag
from os.path import isdir


class JSONConfigsParser(IConfigsParser):
    def __init__(self, dictionary):
        self.options = self.get_options(dictionary)
        self.filetypes = self.get_filetypes(dictionary)
        self.backup_path = "C:\\Users\\Ori\\Desktop\\dst" if self.is_enabled(OptionsFlag.TEST_MODE) else dictionary.get(
            "backupPath")
        self.source_path = "C:\\Users\\Ori\\Desktop\\src" if self.is_enabled(OptionsFlag.TEST_MODE) else dictionary.get(
            "sourcePath")
        self.backcopy_path = "C:\\Users\\Ori\\Desktop\\src" if self.is_enabled(
            OptionsFlag.TEST_MODE) else dictionary.get("backCopyPath")

    @staticmethod
    def from_json(filepath):
        with open(filepath) as config_file:
            configs = json.load(config_file)
        return JSONConfigsParser(configs)

    def get_options(self, dictionary):
        flags = OptionsFlag.NONE
        if dictionary.get("testMode", False):
            flags |= OptionsFlag.TEST_MODE
        if dictionary.get("enableBackup", False):
            flags |= OptionsFlag.COPY_ENABLED
        if dictionary.get("enableBackCopy", False):
            flags |= OptionsFlag.BACKCOPY_ENABLED
        if dictionary.get("recursiveSearch", False):
            flags |= OptionsFlag.RECURSIVE_SEARCH
        return flags

    def get_filetypes(self, dictionary):
        filetypes = FileTypeFlag.NONE
        filetype_list = dictionary.get("filetypes", [])
        for ft in filetype_list:
            if ft == "all":
                return FileTypeFlag.ALL_TYPE
            filetypes |= FileTypeFlag.from_string(ft)
        return filetypes

    def validate(self):
        try:
            if isdir(self.backup_path) and isdir(self.source_path) and \
                    (True if not self.is_enabled(OptionsFlag.BACKCOPY_ENABLED) else isdir(self.backcopy_path)):
                print("Configurations loaded succssfully!{}".format(
                    "\nRunning in test mode.\n" if self.is_enabled(OptionsFlag.TEST_MODE) else "\n"))
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
        except:
            print("There was an error validating the configurations. The program has exited.")
            return False

    def is_enabled(self, option: OptionsFlag) -> bool:
        return bool(self.options & option)
