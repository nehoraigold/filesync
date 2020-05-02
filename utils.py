import typing
import re
from enum import Flag, auto

def print_header(text: str) -> None:
    length = len(text)
    padding = 5
    border = "+" + "-" * padding + "-"*length + "-" * padding + "+"
    title = "\n|" + " " * padding + text + " " * padding + "|\n"
    header = "\n" + border + title + border
    print(header)


def get_regex(patterns: typing.List[str]):
    if len(patterns) == 0:
        return None
    return re.compile("({})".format("|".join(patterns)))


class OptionsFlag(Flag):
    NONE = 0
    HELP = auto()
    TEST_MODE = auto()
    RECURSIVE_SEARCH = auto()
    COPY_ENABLED = auto()
    BACKCOPY_ENABLED = auto()
    SPECIFIC_FILETYPE = auto()

    @staticmethod
    def from_string(arg: str) -> "OptionsFlag":
        flag_to_patterns_map = {
            OptionsFlag.HELP: ["^\-\-help$", "^\-h$"],
            OptionsFlag.TEST_MODE: ["^\-\-test\-mode$", "^\-t"],
            OptionsFlag.RECURSIVE_SEARCH: ["^\-\-recursive$", "^\-r$"],
            OptionsFlag.BACKCOPY_ENABLED: ["^\-\-backcopy$", "^\-b"],
            OptionsFlag.COPY_ENABLED: ["^\-\-copy$", "^\-c$"],
            OptionsFlag.SPECIFIC_FILETYPE: ["^\-\-filetype$", "^\-f"],
        }

        for option, patterns in flag_to_patterns_map.items():
            repr(patterns)
            if get_regex(patterns).search(arg):
                return option
        if arg[0] == "-":
            print("Cannot reconcile unknown flag {}, ignoring".format(arg))
        return OptionsFlag.NONE


class FileTypeFlag(Flag):
    NONE = 0
    IMAGE_TYPE = auto()
    AUDIO_TYPE = auto()
    VIDEO_TYPE = auto()
    ALL_TYPE = IMAGE_TYPE | AUDIO_TYPE | VIDEO_TYPE

    @staticmethod
    def from_string(arg: str) -> "FileTypeFlag":
        filetype_to_patterns_map = {
            FileTypeFlag.IMAGE_TYPE: ["^image$", "^photo$", "^pic.+$"],
            FileTypeFlag.AUDIO_TYPE: ["^audio$", "^music$", "^sound$"],
            FileTypeFlag.VIDEO_TYPE: ["^video$", "^movie$"]
        }

        for filetype, patterns in filetype_to_patterns_map.items():
            if get_regex(patterns).search(arg):
                return filetype
        return FileTypeFlag.NONE

FILETYPE_TO_SUFFIX = {
    FileTypeFlag.IMAGE_TYPE: [".jpg", ".jpeg", ".gif", ".png"],
    FileTypeFlag.VIDEO_TYPE: [".mov", ".wav"],
    FileTypeFlag.AUDIO_TYPE: [".m4a", ".mp3", ".aif", ".wav", ".aac", ".m4p", ".wma"]
}

def print_help_screen():
    print('''
The FileSync backup CLI enables you to run an analysis of files in two directories including comparing them and copying them. You can use the program either with flags as a CLI or by supplying the program with a configuration file.

With a configuration file:

filesync <configs.json>

As a CLI:

filesync -c -r -f <filetype> -b <backcopy dir> <src> <dst>

CLI Flags:
    --help, -h:         Displays this help screen

    --copy, -c:         Enables the copy option from the src 
                        to dst folder

    --backcopy, -b:     Enables copying folders from the dst 
                        to a specified backcopy folder

    --recursive, -r:    When analyzing and copying, searches 
                        in src folder recursively for matching files

    --filetype, -f:     Transfer only specific file types (image, 
                        video, music), otherwise copies all filetypes
''')