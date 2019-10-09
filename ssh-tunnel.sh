#! /bin/bash

A=1

while [ $A == 1 ]
do
ps aux | grep ssh | grep "6666:localhost:22 ashokraja@ashokrajar.isa-geek.net" 2> /dev/zero > /dev/zero

if [ $? -ne 0 ];then
	echo "Starting "
	ssh -R 6666:localhost:22 ashokraja@ashokrajar.isa-geek.net
else
	echo "Already Running"
	sleep 120
fi
done
