#!/usr/bin/env python

# from win32file import CreateFile, SetFileTime, GetFileTime, CloseHandle 

import exifread
import sys, os, re, time, functools


def update_timestamp ( fn ):
    TIMESTAMP = "EXIF DateTimeOriginal"
    with open(fn, 'rb') as fh:
        tags = exifread.process_file(fh)
        stamp = tags[TIMESTAMP]
        t = time.mktime(time.strptime(str(stamp), '%Y:%m:%d %H:%M:%S'))
        os.utime(fn, (t,t))
        print ("updated {} to {}".format(fn, stamp))


def walk_top ( top ):
    for (dirpath, dirnames, filenames) in os.walk(top):
        for base in filter(functools.partial(re.match, "(?i).*jpe?g$"),
                           filenames):
            fn = os.path.join(dirpath, base)
            try:
                update_timestamp(fn)
            except Exception as ex:
                print ("ERROR: unable to update {}'s timestamp: {}"
                       .format(fn, repr(ex)))
                
def main ():
    if len(sys.argv)<2:
        print ("usage: exif-jpeg-timestamper.py PHOTOS-DIRECTORY")
        exit(1)

    top = sys.argv[1]
    walk_top(top)

if __name__ == '__main__':
    main()
