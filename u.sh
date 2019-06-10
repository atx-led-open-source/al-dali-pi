#!/bin/bash
mymac=$(ifconfig | grep 'ether ' | sed '2!d' $myip | cut -d ' ' -f 10 )
wget -nv -O DALI.tar http://atxled.com/Pi/DALI.tar?mac=$mymac
tar -x -f DALI.tar
rm DALI.tar
rm u.sh
wget -nv http://atxled.com/Pi/u.sh
sudo chmod +x u.sh
cd Desktop
./DALI.sh
