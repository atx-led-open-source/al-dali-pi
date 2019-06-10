#!/bin/bash

BASE=`realpath $0`
BASE=`dirname $BASE`
cd $BASE

# Upgrade system packages
sudo apt-get update
sudo apt-get upgrade
sudo apt autoremove

# Install DALI monitor script to desktop
ln -s $BASE/DALI_Monitor.py ~/Desktop/DALI_Monitor.py

# Install NGINX and PHP
sudo apt-get install nginx php-fpm

# Configure NGINX to use PHP, then start NGINX
ln -s /var/www/html html
rm /etc/nginx/sites-enabled/default
cp nginx-conf/php.conf /etc/nginx/sites-available/
ln -s /etc/nginx/sites-available/php.conf /etc/nginx/sites-enabled/php.conf

sudo /etc/init.d/nginx start

# Enable serial port, but not serial console
# The raspi-config script is kinda weird, and isn't documented much. The first arg has to be 2 and not 1
# for some reason...
echo 'enabling serial port in Pi Config...'
sudo raspi-config nonint do_serial 2 0

echo ''
echo ''
echo "update anytime with 'git pull'"
