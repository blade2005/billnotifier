#!/usr/bin/python
'''Print account information'''
import os
import mintapi
import ConfigParser
import sys

CONFIGFILE = os.environ['HOME'] + '/.config/bill_notify/config.conf'
CONFIG = ConfigParser.ConfigParser()
if os.path.exists(CONFIGFILE):
    CONFIG.read(CONFIGFILE)
else:
    print "Missing %s. Exiting." % (CONFIGFILE)
    sys.exit(1)
CONFIG = dict(CONFIG.items('billnotify'))


def main():
    '''Main'''
    if CONFIG['mintuser'] and CONFIG['mintpassword']:
        mint = mintapi.Mint(CONFIG['mintuser'], CONFIG['mintpassword'])
        for bank in mint.get_accounts():
            print (
                "Display Name: %(fiLoginDisplayName)s\n"
                "Account Name: %(accountName)s\n"
                "Bank Name: %(fiName)s\n"
                "Id: %(id)s\n"
                "Balance: %(value)s\n"
            ) % bank

if __name__ == "__main__":
    main()
