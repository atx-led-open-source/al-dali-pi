#!/bin/bash

set -e

BASE=`realpath $0`
BASE=`dirname $BASE`
cd $BASE

echo 'Setting up cron boomerang service...'

sudo cp cron-boom.service /lib/systemd/system/
sudo chmod 644 /lib/systemd/system/cron-boom.service
sudo systemctl daemon-reload
sudo systemctl enable cron-boom.service
sudo systemctl start cron-boom.service
