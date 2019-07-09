#!/bin/bash

set -e

PHP_VER=7.0

BASE=`realpath $0`
BASE=`dirname $BASE`
cd $BASE

if [ "$1" = "--no-update-packages" ]; then
    echo "skipping package update"
else
    # Upgrade system packages
    sudo apt-get -y update
    sudo apt-get -y upgrade
    sudo apt autoremove
fi

# Install DALI monitor script to desktop
echo "$BASE/DALI/DALI_Monitor.py" > ~/Desktop/DALI.sh
chmod +x ~/Desktop/DALI.sh

# Install NGINX and PHP
sudo apt-get -y install nginx php-fpm

# Configure NGINX to use PHP, then start NGINX
sudo ln -s $BASE/C4.php /var/www/html/C4.php || true
sudo rm /etc/nginx/sites-enabled/default || true
sudo cp nginx-conf/php.conf /etc/nginx/sites-available/
sudo ln -s $BASE/nginx-conf/index.nginx-debian.html /var/www/html/
sudo ln -s /etc/nginx/sites-available/php.conf /etc/nginx/sites-enabled/php.conf || true

sudo sed -iOLD 's/user = www-data/user = pi/' /etc/php/$PHP_VER/fpm/pool.d/www.conf || true
sudo sed -iOLD 's/group = www-data/group = pi/' /etc/php/$PHP_VER/fpm/pool.d/www.conf || true

sudo /etc/init.d/php$PHP_VER-fpm restart

sudo /etc/init.d/nginx start
sudo /etc/init.d/nginx reload

# Enable serial port, but not serial console
# The raspi-config script is kinda weird, and isn't documented much. The first arg has to be 2 and not 1
# for some reason...
echo 'enabling serial port in Pi Config...'
sudo raspi-config nonint do_serial 2 0

echo ''
echo ''
echo "update anytime with 'git pull'"
