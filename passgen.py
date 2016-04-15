#!/usr/bin/env python
# -*- coding: utf-8 -*-

import hmac
import hashlib
import base64
import getpass
import sys

password_length = 12

# Mapping from hosts to version numbers
hosts =\
{
    "engine01.club.cc.cmu.edu" : "1"
}

try:
    input = raw_input
except NameError:
    pass

def passgen(master, hostname, version):
    message = (hostname + version).encode("utf-8")
    secret = master.encode("utf-8")
    digest = hmac.new(message, secret, digestmod=hashlib.sha256).digest()
    password = base64.b64encode(digest)[:password_length]
    if isinstance(password, bytes): # Python 3
        password = password.decode("utf-8")
    return password

def main():
    try:
        print("Computer club machine password generation utility")
        print("Run on secure, unshared machines only")
        print("Make sure nobody is shoulder surfing")
        master = getpass.getpass()
        if not master:
            print("Missing password")
            sys.exit(1)
        hostname = input("Enter full hostname: ")
        if not hostname:
            print("Missing hostname")
            sys.exit(1)
        version = hosts[hostname]
        if not hosts[hostname]:
            print("Host not found")
            sys.exit(1)
        print(passgen(master, hostname, version))
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    sys.exit(main())
