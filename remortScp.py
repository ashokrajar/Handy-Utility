#! /usr/bin/python
import sys
import paramiko
import threading
from time import sleep
from optparse import OptionParser


def myssh_client(host, hosttype, cmd):

    # remote open the netcat listener on the host
    sshconn = paramiko.SSHClient()
    sshconn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    sshconn.connect(host)
    try:
        # Exec the command
        stdin, stdout, stderr = sshconn.exec_command(cmd)
    except paramiko.SSHException as e:
        print(e)

    # get the stderr & stdout
    ssherr = stderr.read()
    sshout = stdout.read()

    # close the connection
    sshconn.close()

    if len(ssherr) == 0:
        if hosttype == 's':
            print("%s \t \t | \t COMPLETED \t |" % host)
    else:
        print("Error Occured : Debug Output\n")
        # print ssherr, len(ssherr)


if __name__ == '__main__':
    # command line argument parser
    argparser = OptionParser(version="%prog" + "0.1")
    argparser.add_option("-s", "--shost", action="store", type="string",
                         dest="srchosts", help="List of Source HostNames "
                                               "separated by commas",
                         metavar="host1.dom.com,host2.dom.com")
    argparser.add_option("-t", "--thost", action="store", type="string",
                         dest="dsthosts", help="List of Target HostNames "
                                               "separated by commas",
                         metavar="host1.dom.com,host2.dom.com")
    argparser.add_option("-p", "--port", action="store", type="int",
                         dest="ncport", default=4000,
                         help="NetCat port number which has to be opened on "
                              "Target HostNames.  Default=4000",
                         metavar="4999")
    # argparser.add_option("-f", "--sfile", action="store", type="string",
    #                      dest="srcPath", help="Obsolute file||directory Path "
    #                                           "on the Source Host",
    #                      metavar="/home/ashokr/fileORdir_tocopy")
    (argopt, args) = argparser.parse_args()

    if not (argopt.srcHosts and argopt.dstHosts):
        print("Error : Source Hostnames and Target Hostnames are mandatory"
              "\n\nUsage : remoteScp.py --help\n")
        sys.exit(1)

    dst_hosts = argopt.dsthosts.split(',')  # get Target hosts list
    src_hosts = argopt.srchosts.split(',')  # get Source hosts list
    nc_port = str(argopt.ncport)	 # get the netcat #port
    src_path = "movie"  # get the obsolute file/dir path on the source Host

    dsthost_count = len(dst_hosts)
    srchost_count = len(src_hosts)

    # check if the Source & Target hosts count are the same
    if dsthost_count == srchost_count:
        # For each Target Host open netcat listner and file tranfer netcat
        # client in the respective Source Host
        for i in range(0, dsthost_count):
            # open netcat listner on target host
            dstcmd = "nc -v -l %s | tar xvf -" % nc_port
            hosttype = 't'
            dst_client_thread = threading.Thread(target=myssh_client,
                                                 args=(dst_hosts[i], hosttype,
                                                       dstcmd))
            dst_client_thread.start()

            # Wait for target host to initialize netcat listener
            sleep(5)

            # Connect to the source hosts netcat session and
            # start the file transfer
            src_cmd = "tar cf - %s | nc -v %s %s" % (src_path, dst_hosts[i],
                                                     nc_port)
            hosttype = 's'
            src_client_thread = threading.Thread(target=myssh_client,
                                                 args=(src_hosts[i], hosttype,
                                                       src_cmd))
            src_client_thread.start()

        dst_client_thread.join()
        # srcClientThread.join()

    else:
        print("Error : Source and Target Hosts count Mismatch")
        sys.exit(1)
