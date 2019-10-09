#! /bin/bash

ping -c 3 10.66.192.207 2> /dev/zero > /dev/zero
if [ $? == 0 ];then
    rsync -larh weaklearn-lm:~/Music/ ~/Music/ 
    echo "Music Synced. Status Code $?"
else
    echo "Music Not Synced"
fi
