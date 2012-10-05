#! /usr/bin/python

### import modules ###
from xml.etree import ElementTree
from progressbar import ProgressBar, SimpleProgress
import os, sys, shutil
from optparse import OptionParser
from time import sleep



# method to decode filename
def decodeFileName(fileName):
	'''decode the given fileName to ASCII Character

	return decoded string'''
	
	name = fileName.replace('%20', ' ')		# decode the spaces
	name = name.replace('%5B', '[')			# decode the [
	name = name.replace('%5D', ']')			# decode the ]

	return name


# method to index the Library
def indexTracks(itunesLibrary):
	'''returns a dictionary [trackid : file_location]'''

	trackDict = {}
	
	# find all the tracks element
	trackList = itunesLibrary.findall('dict/dict/dict')

	# Iterate through each track element and create a dictionary [trackid : file_location]
	for track in trackList:
		# get the trackid
		iterElememt = list(track.iter('integer'))
		trackId = iterElememt[0].text

		# get the track location
		iterElememt = list(track.iter('string'))
		trackPath = iterElememt[-1].text

		# Build the dictionary
		trackDict[trackId] = trackPath

	return trackDict

# method to get list of absolute file path for the given playlist name
def getFilePath(itunesLibrary, trackIndex, searchStr):
	'''returns absolute filepath as a list fetching it from the trackIndex'''

	fileList = []
	# fetch all file list form the playlists
	playLists = itunesLibrary.findall('dict/array/dict')

	# Iterate through each playlist
	for playList in playLists:
		# Get the playlist name form the string element
		iterElement = list(playList.iter('string'))
		playListName = iterElement[0].text

		# if playlist match the given playlist
		if playListName == searchStr:

			# Search for all the Tracks in the given playlist
			trackLists = list(playList.iter('integer'))
			trackLists.pop(0)
			# Iterate through the result element list to fetch the track id to fetch the track file path
			for track in trackLists:
				# Get the trackid from the playlist
				trackId = track.text
				# fetch the file path form the index with the trackid
				filePath = trackIndex[trackId]
				filePath = filePath.replace('file://localhost','')		# get the absolute path
				filePath = decodeFileName(filePath)						# decode the filename
				# append th filepath to the list
				fileList.append(filePath)

	return fileList


# method to copy file from source to destination 
def syncFileToDest(sourceFiles, destFolder):
	'''copies to the destination folder if file doesn't exit

	return True on success'''

	for sourceFile in sourceFiles:
		
		fileName = sourceFile.split('/')[-1]		# split file name from absolute path

		# check if the file doesn't exist on the destination
		if not os.path.isfile(destFolder + '/' + fileName):
			# copy file to destination
			try:
				shutil.copy(sourceFile, destFolder)
			except IOError, e:
				print "Sync Failed : ", e
				sys.exit(1)
			except KeyboardInterrupt:
				print "Sync Stopped by a Human"
				sys.exit(1)
			else:
				print "Synced : ", fileName

	return True


### Main Code ###
if __name__ == '__main__':

	# Command Line Arguments Parser
	cmdParser = OptionParser(version = "%prog " + "0.1")
	cmdParser.add_option("-p", "--playlist", action = "store", type = "str", dest = "playList", help = "Name of the Play List")
	cmdParser.add_option("-d", "--dest", action = "store", type = "str", dest = "destFolder", help = "Absolute Destination Folder Path to Sync Music")
	(cmdOptions, cmdArgs) = cmdParser.parse_args()

	# Check cmd arguments
	if not (cmdOptions.playList and cmdOptions.destFolder):
		cmdParser.print_help()
		sys.exit(1)

	playList = cmdOptions.playList
	destFolder = cmdOptions.destFolder

	# iTunes Library Path
	itunesLibFile = os.getenv('HOME') + "/Music/iTunes/iTunes Music Library.xml"

	# Check if file exists
	if os.path.isfile(itunesLibFile):
		# Spawn a separate process to parse
		print "Processing iTunes Library ....."
		itunesLibrary = ElementTree.parse(itunesLibFile)
	else:
		print "Error : iTunes Library not Found"
		sys.exit(1)

	# Beautify with progress bars
	# while(process.is_alive() == True):
	# 	for I in range(2):
	# 		sys.stdout.write("(|)\r")
	# 		sys.stdout.flush()
	# 		sleep(0.1)
	# 		sys.stdout.write("(/)\r")
	# 		sys.stdout.flush()
	# 		sleep(0.1)
	# 		sys.stdout.write("(-)\r")
	# 		sys.stdout.flush()
	# 		sleep(0.1)
	# 		sys.stdout.write("(\\)\r")
	# 		sys.stdout.flush()
	# 		sleep(0.1)

	# recieve and store the parsed object
	# itunesLibrary = parent_conn.recv()
	# join the process
	# process.join()

	# index the library as a key value pair
	# dictionary [trackid : file_location]
	trackIndex = indexTracks(itunesLibrary)

	# get list of absolute file path for the given playlist name
	fileList = getFilePath(itunesLibrary, trackIndex, playList)

	# copy to destination
	print("Syncing Music to %s" % destFolder) 
	syncFileToDest(fileList, destFolder)
		


