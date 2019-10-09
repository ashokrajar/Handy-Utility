#! /bin/bash

ping -c 3 10.66.192.207 2> /dev/zero > /dev/zero
if [ $? == 0 ];then
    rsync -larhv --delete-after /nfs/workspace/ /home/ashokr/workspace/
    echo "WorkSpace Synced. Status Code $?"
else
    echo "WorkSpace Not Synced"
fi
