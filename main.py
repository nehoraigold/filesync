import sys
from utils import OptionsFlag, print_help_screen, print_header
from configs_parser_factory import ConfigsParserFactory
from analyzer import Analyzer
from copier import Copier

def main():
    print_header("FILESYNC BACKUP PROGRAM")
    configs = ConfigsParserFactory.create(sys.argv[1:])
    if configs.is_enabled(OptionsFlag.HELP):
        print_help_screen()
        return exit(0)
    if not configs.validate():
        print("\nThere was an issue validating the configurations. Terminating program.")
        return exit(0)
    analyzer = Analyzer(configs)
    dst_files = analyzer.get_backup_files()
    src_files = analyzer.get_source_files()
    analyzer.compare_directories()
    summary = ""
    if analyzer.files_to_backup > 0 and configs.is_enabled(OptionsFlag.COPY_ENABLED):
        print_header("COPYING TO BACKUP")
        print("Starting copying process...\n")
        copier = Copier(configs.source_path, configs.backup_path, src_files, dst_files, analyzer.files_to_backup)
        backed_up_count = copier.copy()
        summary += "Backed up a total of {} files!".format(backed_up_count)
    if analyzer.files_to_backcopy > 0 and configs.is_enabled(OptionsFlag.BACKCOPY_ENABLED):
        print_header("COPYING TO LOCAL")
        print("Starting copying process...")
        copier = Copier(configs.backup_path, configs.backcopy_path, dst_files, src_files, analyzer.files_to_backcopy)
        backcopied_count = copier.copy()
        summary += "Copied a total of {} files to your local!".format(backcopied_count)
    if summary and (configs.is_enabled(OptionsFlag.BACKCOPY_ENABLED) or configs.is_enabled(OptionsFlag.COPY_ENABLED)):
        print_header("SUMMARY")
        print(summary)
    print("\nComplete!")
    return

if __name__=="__main__":
    main()
