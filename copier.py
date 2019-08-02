import os
from shutil import copyfile

class Copier():
    def __init__(self, sourcePath, destinationPath, sourceDict, destinationDict, number):
        self.source_path = sourcePath
        self.destination_path = destinationPath
        self.source_dict = sourceDict
        self.destination_dict = destinationDict
        self.total = number
    
    def copy(self):
        count = 0
        for filename, filepath in self.source_dict.items():
            if not self.destination_dict.get(filename):
                count += 1
                print("Copying {} of {}... ".format(count, self.total), end="")
                copyfile(filepath, os.path.join(self.destination_path, filename))
                self.destination_dict[filename] = self.destination_path
                print("done!")
        if count != self.total:
            print("There was an issue...")
        print("Complete!\n")
        return count
