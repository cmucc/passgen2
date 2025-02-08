#!/usr/bin/python3
# -*- coding: utf-8 -*-

import hmac
import hashlib
import base64
import getpass
import sys
import argparse

password_length = 12

# Increment this version number when changing the room
default_version = "1"
# Map special hosts to other version numbers
special_hosts =\
{
    "contrib-cgi" : "2",
    "switch-01" : "3",
}

try:
    input = raw_input
except NameError:
    pass

def passgen(master, hostname, version):
    message = (hostname + version).encode("utf-8")
    secret = master.encode("utf-8")
    digest = hmac.new(message, secret, digestmod=hashlib.sha256).digest()
    password = base64.b64encode(digest)[:password_length].decode("utf-8")
    return password

def main():
    parser = argparse.ArgumentParser(prog='passgen', description='Computer Club machine password generation utility', fromfile_prefix_chars='@')
    parser.add_argument('-f', help='only ask for master password once (don\'t use this when generating new passwords)', dest='prompt_twice', action='store_false')
    parser.add_argument('host_list', nargs=argparse.REMAINDER, help='list of hosts')
    args = parser.parse_args()
    hosts = args.host_list

    try:
        print("Computer Club machine password generation utility")
        print("Run on secure, unshared machines only")
        print("Make sure nobody is shoulder surfing")
        print("")
        master = getpass.getpass("  Master password: ")
        if not master:
            print("Missing password")
            sys.exit(1)
        if args.prompt_twice:
            master2 = getpass.getpass("Re-enter password: ")
            if not master == master2:
                print("Unmatching password")
                sys.exit(1)

        # Request a hostname if none were provided at command line.
        if len(hosts) == 0:
            print("")
            hostname = input("         Hostname: ")
            if not hostname:
                print("Missing hostname")
                sys.exit(1)
            hosts.append(hostname)

        print("")
        for hostname in hosts:
            hostname = hostname.lower().split('.')[0]   # Canonicalize hostname
            version = default_version
            if hostname in special_hosts:
                version = special_hosts[hostname]
            print("%s : %s  \t%s" % (hostname, version, passgen(master, hostname, version)))
        print("")
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    sys.exit(main())
