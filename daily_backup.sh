#! /bin/bash

ping -c 3 10.66.192.207 2> /dev/zero > /dev/zero
if [ $? == 0 ];then
    cd /home/backup
    find /home/backup -mtime +10 -exec rm -rf {} \;
    tar -jcpvf /home/backup/daily_`date "+%d-%m-%Y"`.tar.bz2 /nfs/workspace ~/dev_local ~/.bash* ~/.vimrc ~/.cvsrc ~/.screenrc* ~/bin ~/.tsclient ~/.subversion ~/.ssh ~/.push 
    echo "Backup Executed. Status Code $?"
else
    echo "Backup not Taken"
fi
