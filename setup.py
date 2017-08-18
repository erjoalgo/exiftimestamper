import sys
from setuptools import setup

setup(
    name='exiftimestamper',
    version='2016.11.27',
    author = "Ernesto Alfonso",
    author_email = "erjoalgo@gmail.com",
    # url='https://github.com/jrfonseca/gprof2dot',
    description="""A command-line tool to update jpeg file timestamps
    based on their 'EXIF DateTimeOriginal' metadata tag """,
    long_description="""A command-line tool to update jpeg file timestamps
    based on their 'EXIF DateTimeOriginal' metadata tag """,
    license="LGPL",

    py_modules=['exiftimestamper'],
    entry_points=dict(console_scripts=['exiftimestamper=exiftimestamper:main']),
    install_requires=['exifread']
)