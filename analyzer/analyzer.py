import typing
import os
from utils.utils import OptionsFlag, FileTypeFlag, FILETYPE_TO_SUFFIX
from utils import utils


class Analyzer:
    def __init__(self, configs: "IConfigsParser"):
        print("Starting analysis...")
        self.configs = configs
        self.suffixes = self.get_allowed_suffixes()
        self.source_dict: typing.Dict[str, str] = dict()
        self.backup_dict: typing.Dict[str, str] = dict()
        self.duplicates_flag = False
        self.populate_dictionary(configs.source_path, self.source_dict)
        self.populate_dictionary(configs.backup_path, self.backup_dict)
        self.files_to_backup = 0
        self.files_to_backcopy = 0
    
    def compare_directories(self):
        for file in set(list(self.backup_dict.keys()) + list(self.source_dict.keys())):
            in_backup = file in self.backup_dict.keys()
            in_source = file in self.source_dict.keys()
            if in_backup and in_source:
                continue
            elif in_backup and not in_source:
                self.files_to_backcopy += 1
            elif in_source and not in_backup:
                self.files_to_backup += 1

        utils.print_header("ANALYSIS SUMMARY")
        print("There are {} files in your source destination, {} of which need backup."
            .format(len(self.source_dict.keys()), self.files_to_backup))
        if self.files_to_backup > 0 and not self.configs.is_enabled(OptionsFlag.COPY_ENABLED):
            print("Backup is disabled. The {} files will not be backed up.".format(self.files_to_backup))
        print("There are {} files in your backup destination, {} of which you don't have locally."
            .format(len(self.backup_dict.keys()), self.files_to_backcopy))
        if self.files_to_backcopy > 0 and not self.configs.is_enabled(OptionsFlag.BACKCOPY_ENABLED):
            print("Backcopy is disabled. The {} files will not be copied to your local directory.".format(self.files_to_backcopy))        

    def get_source_files(self):
        return self.source_dict
    
    def get_backup_files(self):
        return self.backup_dict
        
    def populate_dictionary(self, filepath, dictionary) -> None:
        with os.scandir(filepath) as it:
            for entry in it:
                if entry.is_file() and self.has_suffix(entry.name):
                    if dictionary.get(entry.name):
                        if not self.duplicates_flag:
                            self.duplicates_flag = True
                            utils.print_header("DUPLICATES")
                        print("Possible duplicate of '{}' found!".format(entry.name))
                        print(" ==> {}\n ==> {}\n".format(entry.path, dictionary.get(entry.name)))
                    dictionary[entry.name] = entry.path
                elif entry.is_dir() and self.configs.is_enabled(OptionsFlag.RECURSIVE_SEARCH):
                    self.populate_dictionary(entry.path, dictionary)
        
    def get_allowed_suffixes(self):
        suffix_list = []
        for filetype, suffixes in FILETYPE_TO_SUFFIX.items():
            if self.configs.filetypes & filetype:
                suffix_list += suffixes
        return suffix_list

    def has_suffix(self, entryName):
        if self.configs.filetypes == FileTypeFlag.ALL_TYPE:
            return True
        return any([filetype in entryName for filetype in self.suffixes])