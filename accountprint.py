#!/usr/bin/python
import os
import mintapi
import ConfigParser

CONFIGFILE = os.environ['HOME'] + '/.config/bill_notify/config.conf'
CONFIG = ConfigParser.ConfigParser()
if os.path.exists(CONFIGFILE):
    CONFIG.read(CONFIGFILE)
else:
    print "Missing %s. Exiting." % (CONFIGFILE)
    sys.exit(1)

CONFIG = dict(CONFIG.items('billnotify'))
if CONFIG['mintuser'] and CONFIG['mintpassword']:
    mint = mintapi.Mint(CONFIG['mintuser'], CONFIG['mintpassword'])
    bankinfo = mint.get_accounts()
    avaliable_balance = 0
    for bank in bankinfo:
        print (
            "Display Name: %(fiLoginDisplayName)s\n"
            "Account Name: %(accountName)s\n"
            "Bank Name: %(fiName)s\n"
            "Id: %(id)s\n"
            "Balance: %(value)s\n"
        ) % bank