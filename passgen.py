import hashlib
import hmac
import base64
import getpass
import sys

def passgen(master, hostname):
  message = hostname.encode('utf-8')
  secret = master.encode('utf-8')
  return base64.b64encode(hmac.new(message, secret, digestmod=hashlib.sha512).digest()).decode('utf-8')

def main():
  print("Computer club machine password generation utility")
  print("Run on secure, unshared machines only")
  print("Make sure nobody is shoulder surfing")
  master = getpass.getpass()
  hostname = input("Enter hostname: ")
  print(passgen(master, hostname))

if __name__ == "__main__":
  sys.exit(main())
