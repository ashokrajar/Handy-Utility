#!/usr/bin/env python
# -*- coding: utf-8 -*-

### import modules ###
import os
import sys
import shutil
from time import sleep
import argparse
from xml.etree import ElementTree
from progressbar import ProgressBar, SimpleProgress


# method to decode filename
def decode_file_name(filename):
    """decode the given fileName to ASCII Character

    return decoded string"""

    name = filename.replace('%20', ' ')        # decode the spaces
    name = name.replace('%5B', '[')            # decode the [
    name = name.replace('%5D', ']')            # decode the ]

    return name


# method to index the Library
def index_tracks(itunesLibrary):
    '''returns a dictionary [trackid : file_location]'''

    trackdict = { }

    # find all the tracks element
    tracklist = itunesLibrary.findall('dict/dict/dict')

    # Iterate through each track element and create a dictionary [trackid : file_location]
    for track in tracklist:
        # get the trackid
        iterelememt = list(track.iter('integer'))
        trackid = iterelememt[0].text

        # get the track location
        iterelememt = list(track.iter('string'))
        trackpath = iterelememt[-1].text

        # Build the dictionary
        trackdict[trackid] = trackpath

    return trackdict


# method to get list of absolute file path for the given playlist name
def get_file_path(ituneslibrary, trackindex, searchstr):
    """returns absolute filepath as a list fetching it from the trackIndex"""

    filelist = []
    # fetch all file list form the playlists
    playlists = ituneslibrary.findall('dict/array/dict')

    # Iterate through each playlist
    for playlist in playlists:
        # Get the playlist name form the string element
        iterelement = list(playlist.iter('string'))
        playlistname = iterelement[0].text

        # if playlist match the given playlist
        if playlistname == searchstr:

            # Search for all the Tracks in the given playlist
            tracklists = list(playlist.iter('integer'))
            tracklists.pop(0)
            # Iterate through the result element list to fetch the track id to fetch the track file path
            for track in tracklists:
                # Get the trackid from the playlist
                trackid = track.text
                # fetch the file path form the index with the trackid
                filepath = trackindex[trackid]
                filepath = filepath.replace('file://localhost', '')        # get the absolute path
                filepath = decode_file_name(filepath)                        # decode the filename
                # append th filepath to the list
                filelist.append(filepath)

    return filelist


# method to copy file from source to destination
def sync_file_to_dest(sourcefiles, destfolder):
    """copies to the destination folder if file doesn't exit

    return True on success"""

    for sourcefile in sourcefiles:

        filename = sourcefile.split('/')[-1]        # split file name from absolute path

        # check if the file doesn't exist on the destination
        if not os.path.isfile(destfolder + '/' + filename):
            # copy file to destination
            try:
                shutil.copy(sourcefile, destfolder)
            except IOError, e:
                print "Sync Failed : ", e
                sys.exit(1)
            except KeyboardInterrupt:
                print "Sync Stopped by a Human"
                sys.exit(1)
            else:
                print "Synced : ", filename

    return True


cmdParser.add_argument('--version', action='version', version='%(prog)s 1.1')
    optionGroup = cmdParser.add_argument_group('General Options')
    optionGroup.add_argument('--outfolder', help='Destination folder to copy the files')

### Main Code ###
if __name__ == '__main__':



    # cmdArgs = cmdParser.parse_args()


    print cmdParser.parse_args(['--help'])

    # # Check cmd arguments
    # if not (cmdOptions.playList and cmdOptions.destFolder):
    #     cmdParser.print_help()
    #     sys.exit(1)
    #
    # playList = cmdOptions.playList
    # destFolder = cmdOptions.destFolder
    #
    # # iTunes Library Path
    # itunesLibFile = os.getenv('HOME') + "/Music/iTunes/iTunes Music Library.xml"
    #
    # # Check if file exists
    # if os.path.isfile(itunesLibFile):
    #     # Spawn a separate process to parse
    #     print "Processing iTunes Library ....."
    #     itunesLibrary = ElementTree.parse(itunesLibFile)
    # else:
    #     print "Error : iTunes Library not Found"
    #     sys.exit(1)
    #
    # # index the library as a key value pair
    # # dictionary [trackid : file_location]
    # trackIndex = index_tracks(itunesLibrary)
    #
    # # get list of absolute file path for the given playlist name
    # fileList = get_file_path(itunesLibrary, trackIndex, playList)
    #
    # # copy to destination
    # print("Syncing Music to %s" % destFolder)
    # sync_file_to_dest(fileList, destFolder)
