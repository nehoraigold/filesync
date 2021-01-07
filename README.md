# File Copier

Ideas for improvement:
* Actual CLI rather than config file, with...
* Flags for all the things in the config file
* Different file types (photos, music, video, etc.)
* Recursive or non recursive searches in folder
* Test mode pretends it does everything but doesn't really
* Verbose mode and less verbose mode

Flags:
* --help, -h: Displays help screen
* --copy, -c: Enables the copy option from the src to dst folder
* --backcopy, -b: Enables copying folders from the dst to third backcopy directory
* --recursive, -r: When analyzing and copying, searches in src folder recursively for matching files
* --filetype, -f: Transfer only specific file types (image, video, music)
* --test-mode, -t: Run in test mode

filesync -c -r -f <filetype> -b <backcopy dir> <src> <dst>