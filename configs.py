import json
from os.path import isdir

class Configs():
    def __init__(self, dictionary):
        self.test_mode = dictionary.get("test", False)
        self.backup_path = "C:\\Users\\Ori\\Desktop\\dst" if self.test_mode else dictionary.get("backupPath")
        self.source_path = "C:\\Users\\Ori\\Desktop\\src" if self.test_mode else dictionary.get("sourcePath")
        self.backcopy_path = "C:\\Users\\Ori\\Desktop\\src" if self.test_mode else dictionary.get("backCopyPath")
        self.backcopy_enabled = dictionary.get("enableBackCopy", False)
        if self.validate_paths():
            print("\nConfigurations loaded succssfully!{}".format("\nRunning in test mode.\n" if self.test_mode else "\n"))
        else:
            msg = "There was an error loading the configuration file.\n\nOne or more of the configured paths is invalid. Have you connected the external hard drive?"
            print("{}\n => Source: {}\n => Backup: {}{}".format(
                msg,
                self.source_path, 
                self.backup_path, 
                "\n => Backcopy: {}".format(self.backcopy_path) if self.backcopy_enabled else ""))
            exit(0)
    
    @staticmethod
    def from_json(filepath):
        with open(filepath) as config_file:
            configs = json.load(config_file)
        return Configs(configs)

    def validate_paths(self):
        try:
            return isdir(self.backup_path) and isdir(self.source_path) and (True if not self.backcopy_enabled else isdir(self.backcopy_path))
        except:
            return False
