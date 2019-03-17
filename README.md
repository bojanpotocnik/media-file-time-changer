# File Time-Attribute Changer

When media files are transferred from e.g. Android device via MTP protocol the creation time attributes are lost. 

However fortunately, as a rule, files contain creation date and time in their names. This script reads this information from the file name of any dropped file (or multiple files) and modifies the file attributes to reflect this data.

There are two versions:
- [set_ctime_to_filename_time.py](set_ctime_to_filename_time.py) changes only _Creation Time_ and leaves _Last Write (Last Modified)_ and _Last Access_ times as as their are.
- [set_times_to_filename_time.py](set_times_to_filename_time.py) changes all time attributes to the creation time read from file name (_Creation Time_, _Last Write/Modified_ and _Last Access_ times).

The only difference between those two scripts is on lines 44 and 45.



If drag-and-drop of files to .py scripts does not work for you, you can use [windows-python-file-associator](https://github.com/bojanpotocnik/windows-python-file-associator) to enable this functionality.
