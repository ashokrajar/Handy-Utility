#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Usage: songmeta-mgr.py [OPTIONS]

  MP3 files MetaData(ID3 Tags) updater

Options:
  --folder TEXT    MP3 files location Directory path
  --composer TEXT  Music composer Name
  --help           Show this message and exit.
"""

from __future__ import print_function
import sys
import os
import zipfile

from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
import click


def fetch_mp3_files(folder):
    """
    Search for MP3 files under the directory and return a MP3 file list

    Args:
        folder (str): Absolute path to folder

    Returns:
        list: List of files
    """
    file_list = []
    if os.path.isdir(folder):
        for file_name in os.listdir(folder):
            if file_name.endswith('.mp3'):
                file_list.append("{0:s}/{1:s}".format(folder, file_name))
    else:
        click.echo("Path doesn't exits")
        sys.exit(1)

    return file_list


def list_metadata(folder):
    """
    LIst the ID3 composer tag

    Args:
        folder (str): Absolute path to folder
    """
    for mp3_file in fetch_mp3_files(folder):
        song = MP3(mp3_file, ID3=EasyID3)

        print(song.tags)


def update_metadata(folder, composer):
    """
    Update the ID3 composer tag

    Args:
        folder (str): Absolute path to folder
        composer (str): Composer name
    """
    for mp3_file in fetch_mp3_files(folder):
        song = MP3(mp3_file, ID3=EasyID3)

        # strip '-StarMusiq.Com'
        song_title = song.tags['title']
        if song_title[0].endswith("StarMusiQ.Com"):
            song.tags['title'] = song_title[0][:-14]
            # strip '-VmusiQ.Com'
        elif song_title[0].endswith("-VmusiQ.Com"):
            song.tags['title'] = song_title[0][:-12]

        # insert the composer
        song.tags['performer'] = composer
        song.tags['conductor'] = composer
        song.tags['composer'] = composer
        song.tags['genre'] = ""
        song.save()


def strip_filename_sufix(folder):
    """
    Search for MP3 files under the directory
    Strip unwanted text from mp3 file name.

    Args:
        folder (str): Absolute path to folder
    """
    # strip '-VmusiQ.Com' from file name
    for mp3_file in fetch_mp3_files(folder):
        if mp3_file.endswith("StarMusiQ.Com.mp3"):
            new_filename = mp3_file[:-18] + ".mp3"
            os.rename(mp3_file, new_filename)
        elif mp3_file.endswith("-VmusiQ.Com.mp3"):
            new_filename = mp3_file[:-15] + ".mp3"
            os.rename(mp3_file, new_filename)


@click.command()
@click.option('--folder',
              prompt='MP3 files location',
              help='MP3 files location Directory path')
@click.option('--composer',
              prompt='Composer Name',
              help="Music composer Name")
def main(folder, composer):
    """
    MP3 files MetaData(ID3 Tags) updater

    Args:
        folder (str): Absolute path to folder
        composer (str): Composer name
    """
    # list_metadata(folder)
    update_metadata(folder, composer)
    strip_filename_sufix(folder)


if __name__ == '__main__':
    main()
