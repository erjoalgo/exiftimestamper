#!/usr/bin/env python

from __future__ import print_function

import calendar
import importlib.metadata
import shutil
import subprocess
import exifread
import sys, os, re, time, functools
import argparse

try:
    __version__ = importlib.metadata.version("exiftimestamper")
except importlib.metadata.PackageNotFoundError:
    # running from the source tree, not installed
    __version__ = "unknown"

def exif_timestamp(fn):
    TIMESTAMP_TAGS = ["EXIF DateTimeOriginal",
                      "Image DateTime"]
    with open(fn, 'rb') as fh:
        tags = exifread.process_file(fh)
        for TAG in TIMESTAMP_TAGS:
            stamp = tags.get(TAG)
            if stamp:
                break
        else:
            raise Exception("no date tag in {}: {}"
                            .format(fn, tags.keys()))

        t = time.strptime(str(stamp), '%Y:%m:%d %H:%M:%S')
        # EXIF dates are in the camera's local time
        return time.mktime(t)

def mp4_timestamp(fn):
    # mediainfo --Inform="General;%Encoded_Date%" VID_20170811_221350395-i-did-it-my-way-ryong-il-kiyul.mp4
    # UTC 2017-08-11 14:19:13

    stamp = subprocess.check_output(
        ["mediainfo", "--Inform=General;%Encoded_Date%", fn], text=True)
    stamp = stamp.strip()
    # older mediainfo: 'UTC 2017-08-11 14:19:13'
    # newer mediainfo: '2017-08-11 14:19:13 UTC'
    for fmt in ('%Z %Y-%m-%d %H:%M:%S', '%Y-%m-%d %H:%M:%S %Z'):
        try:
            # the encoded date is in UTC
            return calendar.timegm(time.strptime(stamp, fmt))
        except ValueError:
            pass
    raise ValueError("unrecognized mediainfo date in {}: {!r}".format(fn, stamp))

def media_timestamp(fn):
    if re.match("(?i).*[.]jpe?g$", fn):
        return exif_timestamp(fn)
    elif re.match("(?i).*[.]mp4$", fn):
        return mp4_timestamp(fn)
    else:
        return None

def walk_top(media_directory, quiet, recursive):
    top = media_directory
    print ("walking over '{}'".format(top), file=sys.stderr)
    failed = 0
    total = 0

    for (dirpath, dirnames, filenames) in \
        os.walk(top) if recursive else ((top, [], os.listdir(top)), ):
        for base in filenames:
            fn = os.path.join(dirpath, base)
            try:
                utime = media_timestamp(fn)
                if utime is not None:
                    total += 1
                    stamp = time.strftime('%Y:%m:%d %H:%M:%S',
                                          time.localtime(utime))
                    curr_mtime = os.path.getmtime(fn)
                    if utime != curr_mtime:
                        if not quiet:
                            print ("updating {} to {}".format(fn, stamp))
                        os.utime(fn, (utime, utime))

            except Exception as ex:
                total += 1
                failed += 1
                print ("ERROR: unable to update {}'s timestamp: {}"
                       .format(fn, repr(ex)), file=sys.stderr)

    print ("{}/{} errors"
           .format(failed, total), file=sys.stderr)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("media_directory",
                        help="top-level directory containing images")
    parser.add_argument("--quiet", "-q", action="store_true",
                        help="don't report success")
    parser.add_argument("--recursive", "-r", action="store_true",
                        help="recurisve")
    parser.add_argument("--version", action="version",
                        version=__version__)

    kwargs = vars(parser.parse_args())
    if not shutil.which("mediainfo"):
        print ("WARNING: mediainfo required for mp4 timestamp extraction")

    walk_top(**kwargs)

if __name__ == '__main__':
    main()
