from configs import Configs
from analyzer import Analyzer
from copier import Copier
import utils

def main():
    utils.print_header("MUSIC BACKUP PROGRAM")
    configs = Configs.from_json("config.json")
    analyzer = Analyzer(configs)
    dst_files = analyzer.get_backup_files()
    src_files = analyzer.get_source_files()
    analyzer.compare_directories()
    summary = ""
    if analyzer.files_to_backup > 0 and configs.backup_enabled:
        utils.print_header("COPYING TO BACKUP")
        print("Starting copying process...\n")
        copier = Copier(configs.source_path, configs.backup_path, src_files, dst_files, analyzer.files_to_backup)
        backed_up_count = copier.copy()
        summary += "Backed up a total of {} files!".format(backed_up_count)
    if analyzer.files_to_backcopy > 0 and configs.backcopy_enabled:
        utils.print_header("COPYING TO LOCAL")
        print("Starting copying process...")
        copier = Copier(configs.backup_path, configs.backcopy_path, dst_files, src_files, analyzer.files_to_backcopy)
        backcopied_count = copier.copy()
        summary += "Copied a total of {} files to your local!".format(backcopied_count)
    if summary and (configs.backcopy_enabled or configs.backup_enabled):
        utils.print_header("SUMMARY")
        print(summary)
    print("\nComplete!")
    return

if __name__=="__main__":
    main()
