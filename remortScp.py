#! /usr/bin/python

__version__ = "1.0"
__author__ = "ashokraja.r@gmail.com"


### import modules ###

import sys
import paramiko
import threading
from time import sleep
from optparse import OptionParser



### methods implemetation ###

def mysshClient(host, hostType, cmd):

    # remote open the netcat listener on the host
    mySshClient = paramiko.SSHClient()
    mySshClient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    mySshClient.connect(host)
    try:
        # Exec the command
        mysshStdin, mysshStdout, mysshStderr = mySshClient.exec_command(cmd)
    except paramiko.SSHException, e:
        print e

    # get the stderr & stdout
    remoteErr = mysshStderr.read()
    remoteOut = mysshStdout.read()

    # close the connection
    mySshClient.close()

    if (len(remoteErr) == 0):

        if hostType == 's':
            print "%s \t \t | \t COMPLETED \t |" % (host)
    else:
        print "Error Occured : Debug Output\n"
        # print remoteErr, len(remoteErr)



### Main code ###

if __name__ == '__main__':

    # command line argument parser
    cmdParser = OptionParser(version= "%prog" + __version__)
    cmdParser.add_option("-s", "--shost", action = "store", type = "string", dest = "srcHosts", help = "List of Source HostNames separated by commas", metavar = "host1.dom.com,host2.dom.com")
    cmdParser.add_option("-t", "--thost", action = "store", type = "string", dest = "dstHosts", help = "List of Target HostNames separated by commas", metavar = "host1.dom.com,host2.dom.com")
    cmdParser.add_option("-p", "--tport", action = "store", type = "int", dest = "ncPort", default = 4000, help = "NetCat port number which has to be opened on Target HostNames.  Default = 4000", metavar = "4999")
    # cmdParser.add_option("-f", "--sfile", action = "store", type = "string", dest = "srcPath", help = "Obsolute file||directory Path on the Source Host", metavar = "/home/ashokr/fileORdir_tocopy")
    ( cmdOptions, cmdArgs ) = cmdParser.parse_args()

    if not ( cmdOptions.srcHosts and cmdOptions.dstHosts ):
        print "Error : Source Hostnames and Target Hostnames are mandatory\n\nUsage : remoteScp.py --help\n"
        sys.exit(1)

    dstHosts = cmdOptions.dstHosts.split(',')	# get Target hosts list
    srcHosts = cmdOptions.srcHosts.split(',')	# get Source hosts list
    ncPort = str(cmdOptions.ncPort)				# get the netcat #port
    srcPath = "movie"				# get the Obsolute file||directory Path on the Source Host

    dstHostCount = len(dstHosts)
    srcHostCount = len(srcHosts)

    # check if the Source & Target hosts count are the same
    if dstHostCount == srcHostCount:

        # For each Target Host open netcat listner and file tranfer netcat client in the respective Source Host
        for i in range(0, dstHostCount):

            # open netcat listner on target host
            dstCmd = "nc -v -l %s | tar xvf -" % (ncPort)
            hostType = 't'
            myClientThread = threading.Thread(target=mysshClient, args=(dstHosts[i], hostType, dstCmd))
            myClientThread.start()

            # Wait for target host to initialize netcat listener
            sleep(5)

            # connect to the source hosts netcat session and start the file transfer
            srcCmd = "tar cf - %s | nc -v %s %s" % (srcPath, dstHosts[i], ncPort)
            hostType = 's'
            srcClientThread = threading.Thread(target=mysshClient, args=(srcHosts[i], hostType, srcCmd))
            srcClientThread.start()

        myClientThread.join()
        # srcClientThread.join()

    else:
        print "Error : Source and Target Hosts count Mismatch"
        sys.exit(1)

