#!/bin/bash

mymac=$(ifconfig | grep 'ether ' | sed '2!d' $myip | cut -d ' ' -f 10 )

sudo apt-get update
sudo apt-get upgrade
sudo apt autoremove
wget -nv -O DALI.tar https://atxled.com/Pi/DALI.tar?mac=$mymac
tar -x -f DALI.tar
rm DALI.tar
sudo echo 'python ../DALI_Monitor.py' > Desktop/DALI.sh
sudo chmod +x Desktop/DALI.sh

sudo apt-get install nginx
ln -s /var/www/html html
sudo apt-get install php-fpm

#
# notes
# sudo chmod +x Load.sh
# sudo ./Load.sh
rm u.sh
rm Load.sh
sudo echo 'python DALI_Monitor.py' > m.sh
sudo chmod +x m.sh
wget -nv -O u.sh https://atxled.com/Pi/u.sh
sudo chmod +x u.sh

echo ''
echo ''
echo "update anytime with ./u.sh"
echo ''
echo 'enable serial port in Pi Config'
echo 'disable console in Pi Config'
echo ''
read -p "Press [Enter] key after you have enabled the serial port"
cd Desktop
./DALI.sh
