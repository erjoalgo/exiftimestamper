A command-line tool to set photo and video files' modified times to when they
were taken, so they sort by date in file managers and photo tools.

- JPEG photos: the `EXIF DateTimeOriginal` tag (or `Image DateTime`).
- MP4 videos: the encoded date reported by `mediainfo`, which needs to be
  installed (`$ sudo apt install mediainfo`).

To install:

`$ pip install exiftimestamper`

Update the files in a directory:

`$ exiftimestamper ~/Pictures/trip`

Include subdirectories, and only report errors:

`$ exiftimestamper -r -q ~/Pictures`
