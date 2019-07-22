#!/usr/bin/python3
import logging
import socket
import time

import requests

# Get the mac of the wifi adapter. RPi specific-ish
def get_mac_address():
    with open('/sys/class/net/wlan0/address') as f:
        return f.read().strip().replace(':', '')

# https://stackoverflow.com/questions/166506
def get_ip_address():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.connect(("1.1.1.1", 80))
    ip = sock.getsockname()[0]
    sock.close()
    return ip

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    last_data = None
    while True:
        try:
            mac = get_mac_address()
            ip = get_ip_address()
            data = {'mac': mac, 'ip': ip}
        except Exception as e:
            logging.error('error getting LAN info: %s', e)
            time.sleep(30)
            continue
        # Only send a request if our local ip has changed
        if data == last_data:
            continue

        logging.info('updating boomerang service: %s', data)
        response = requests.get('http://me.atxled.com/up?lan=%s&mac=%s' % (ip, mac))
        if response.status_code != 200:
            logging.info('could not update boomerang service[%s]: %s',
                    response.status_code, response.text)
        else:
            last_data = data

        time.sleep(20*60)
