import datetime
import os
import re
import sys
import win32file
from typing import List, Pattern

import pywintypes
import win32con

__author__ = "Bojan Potočnik"


def do_file(fp: str, ts: datetime.datetime) -> int:
    print(f"Changing ctime/atime/mtime to {ts} for file '{fp}'")

    ctime = ts.timestamp()

    # This https://docs.python.org/3/library/os.html#os.utime only changes atime and ctime.

    # https://stackoverflow.com/questions/4996405/how-do-i-change-the-file-creation-date-of-a-windows-file-from-python

    # Open file and get the handle of it
    # http://timgolden.me.uk/pywin32-docs/win32file__CreateFile_meth.html
    win_file = win32file.CreateFile(
        fp,
        win32con.GENERIC_WRITE,
        0,  # win32con.FILE_SHARE_READ | win32con.FILE_SHARE_WRITE | win32con.FILE_SHARE_DELETE,
        None,
        win32con.OPEN_EXISTING,
        0,  # win32con.FILE_ATTRIBUTE_NORMAL,
        None)

    # Create a PyTime object
    # http://timgolden.me.uk/pywin32-docs/pywintypes__Time_meth.html
    # noinspection PyUnresolvedReferences
    win_time = pywintypes.Time(ctime)

    # Reset the times of the file
    # http://timgolden.me.uk/pywin32-docs/win32file__SetFileTime_meth.html
    win32file.SetFileTime(
        win_file,  # File
        win_time,  # CreationTime - File created time. None for no change.
        None,  # LastAccessTime - File access time. None for no change.
        None  # LastWriteTime - File written time. None for no change.
    )
    win_file.close()

    return 0


def main() -> int:
    files = sys.argv[1:]
    if not files:
        print(f"No files provided", file=sys.stderr)
        return -1

    # This could be `[re.compile(p) for p in [ string patterns... ]]` but PyCharm smart-checks re.compile() strings
    patterns: List[Pattern] = [
        # Modified regex from https://stackoverflow.com/a/47856906/5616255
        re.compile(r".*(?<!\d)"
                   r"(?P<year>20\d{2})(?P<month>\d{2})(?P<day>\d{2})"
                   r"\D?"
                   r"(?P<hours>\d{2})(?P<minutes>\d{2})(?P<seconds>\d{2})"
                   r"(?!\d).*")
    ]

    for fp in files:
        fn = os.path.basename(fp)
        match = None
        for pattern in patterns:
            match = pattern.match(fn)
        if not match:
            print(f"No timestamp information could be extracted from '{fn}' ({fp})", file=sys.stderr)
            return -2
        ts = datetime.datetime(year=int(match.group("year")),
                               month=int(match.group("month")),
                               day=int(match.group("day")),
                               hour=int(match.group("hours")),
                               minute=int(match.group("minutes")),
                               second=int(match.group("seconds")))
        do_file(fp, ts)

    return 0


if __name__ == "__main__":
    ret = main()
    if ret != 0:
        input(f"Exit code is {ret}. Press Enter to close... ")
    exit(ret)
