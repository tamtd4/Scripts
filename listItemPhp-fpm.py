#!/usr/bin/python
import os
import re
import sys

from subprocess import Popen, PIPE


def get_listen_host_port(filepath):
    with open(filepath) as f:
        data = f.read()

    regex = 'listen = (.+)'
    return re.findall(regex, data)[0]

def get_status_path(filepath):
    with open(filepath) as f:
        data = f.read()

    regex = 'pm.status_path = (.+)'
    return re.findall(regex, data)[0]


def get_status(hostport, statuspath, string):
    command = '/usr/local/bin/fcgi.pl %s  "%s?xml" | grep "<%s>" | awk -F\'>|<\' \'{ print $3}\'' \
        % (hostport, statuspath, string )    
    os.system(command)

def main():
    args = sys.argv
    args[1] = "/etc/php-fpm.d/" + args[1] + ".conf"
    hostport = get_listen_host_port(args[1])
    statuspath = get_status_path(args[1]) 
    pool = get_status(hostport,statuspath,args[2])


if __name__ == '__main__':
    main()

