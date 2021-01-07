import typing
from copier.icopier import ICopier


class TestCopier(ICopier):
    def __init__(self,
                 sourcePath: str,
                 destinationPath: str,
                 sourceDict: typing.Dict[str, str],
                 destinationDict: typing.Dict[str, str],
                 number: int):
        self.source_path = sourcePath
        self.destination_path = destinationPath
        self.source_dict = sourceDict
        self.destination_dict = destinationDict
        self.total = number

    def copy(self) -> int:
        count = 0
        for filename, filepath in self.source_dict.items():
            if not self.destination_dict.get(filename):
                count += 1
                print("<<TEST MODE>> Copying {} ({} of {})... ".format(filename, count, self.total), end="")
                self.destination_dict[filename] = self.destination_path
                print("done!")
        if count != self.total:
            print("There was an issue...")
        print("Complete!")
        return count
