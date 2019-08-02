from configs import Configs
from analyzer import Analyzer
from copier import Copier
import utils

def main():
    utils.print_header("MUSIC BACKUP CLI")
    configs = Configs.from_json("config.json")
    analyzer = Analyzer(configs)
    dst_files = analyzer.get_backup_files()
    src_files = analyzer.get_source_files()
    analyzer.compare_directories()
    summary = ""
    if analyzer.files_to_backup > 0:
        utils.print_header("COPYING TO BACKUP")
        if configs.backup_enabled:
            print("Finding files to back up...\n")
            copier = Copier(configs.source_path, configs.backup_path, src_files, dst_files, analyzer.files_to_backup)
            backed_up_count = copier.copy()
            summary += "\nBacked up a total of {} files!".format(backed_up_count)
        else:
            print("Backup is disabled. The {} files will not be backed up.\n".format(analyzer.files_to_backup))
    if analyzer.files_to_backcopy > 0:
        utils.print_header("COPYING TO LOCAL")
        if configs.backcopy_enabled:
            print("Finding files to copy back to local directory...")
            copier = Copier(configs.backup_path, configs.backcopy_path, dst_files, src_files, analyzer.files_to_backcopy)
            backcopied_count = copier.copy()
            summary += "\nCopied a total of {} files to your local!".format(backcopied_count)
        else:
            print("Backcopy is disabled. The {} files will not be copied to your local directory.\n".format(analyzer.files_to_backcopy))
    if summary and (configs.backcopy_enabled or configs.backup_enabled):
        utils.print_header("SUMMARY")
        print("Backup completed successfully!")
        print(summary)
    return

if __name__=="__main__":
    main()
