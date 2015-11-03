#!/usr/bin/python
'''
    Due Date Notifier - Notify VIA email via smtp
'''
# Author: Craig Davis
# Copyright 2015
# LICENSE: GNU v3
from __future__ import with_statement
import datetime
import calendar
import smtplib
import os
import yaml
import ConfigParser
import sys
import mintapi
try:
    from email.mime.text import MIMEText
except ImportError:
    # Python 2.4 (CentOS 5.x)
    from email.MIMEText import MIMEText

notify_day = calendar.THURSDAY
###############################################################################
######################## DO NOT MODIFY BELOW THIS LINE ########################
###############################################################################
CONFIGFILE = os.environ['HOME'] + '/.config/bill_notify/config.conf'
BILLFILE = os.environ['HOME'] + '/.config/bill_notify/bills.yaml.conf'
CONFIG = ConfigParser.ConfigParser()
if os.path.exists(CONFIGFILE):
    CONFIG.read(CONFIGFILE)
else:
    print "Missing %s. Exiting." % (CONFIGFILE)
    sys.exit(1)

CONFIG = dict(CONFIG.items('billnotify'))
CONFIG['to'] = [e.strip() for e in CONFIG['to'].split(',')]


def get_notifications(bills):
    '''Compile list of bills to notify about from main list'''
    curtime = datetime.datetime.now()
    dayofmonth = curtime.day
    daysinmonth = calendar.monthrange(curtime.year, curtime.month)[1]
    week_bills = []
    if calendar.weekday(curtime.year, curtime.month, curtime.day) == notify_day:
        print "Today is %s. Sending emails" % (
            calendar.day_name[notify_day]
        )
        for bill in sorted(bills, key=lambda k: k['duedate']):
            if (
                7 + dayofmonth > bill['duedate'] and
                bill['duedate'] > dayofmonth
                ) or (
                7 + dayofmonth > daysinmonth + bill['duedate'] and
                daysinmonth + bill['duedate'] > dayofmonth
            ):
                week_bills.append(bill)
    else:
        print "Today is not %s. No emails will be sent" % (
            calendar.day_name[notify_day]
        )
    return week_bills


def send_email(subject, message):
    '''Send email via SMTP'''
    msg = MIMEText(message)

    msg['From'] = CONFIG['from']
    # print CONFIG['to']
    msg['To'] = ', '.join(CONFIG['to'])
    msg['Subject'] = subject

    if(CONFIG['ssl']):
        mailer = smtplib.SMTP_SSL(CONFIG['host'], CONFIG['port'])
    else:
        mailer = smtplib.SMTP(CONFIG['port'], CONFIG['port'])

    if(CONFIG['auth']):
        mailer.login(CONFIG['username'], CONFIG['password'])

    mailer.sendmail(CONFIG['from'], CONFIG['to'], msg.as_string())
    mailer.close()


def do_notifications(notifications):
    '''
        Format all the notifications from get_notifications into subject
        and message
    '''
    billstring = []
    if not notifications:
        return False
    weektotal = 0
    for bill in notifications:
        bill['duedate'] = stylish_date(bill['duedate'])
        weektotal += int(bill['amount'])
        billstring.append(
            "%(name)s, %(description)s, Due: $%(amount)s on %(duedate)s" % bill
        )
    billstring = '\n'.join(billstring)
    curtime = datetime.datetime.now()
    message = (
        "Upcoming Bills:\n%(billstring)s\n\n"
        "Total amount of bills due: $%(weektotal)s\n"
    ) % {
        'billstring': billstring,
        'weektotal': weektotal,
    }
    if CONFIG['mintuser'] and CONFIG['mintpassword']:
        mint = mintapi.Mint(CONFIG['mintuser'], CONFIG['mintpassword'])
        bankinfo = mint.get_accounts()
        avaliable_balance = 0
        for bank in bankinfo:
            if int(bank['id']) == int(CONFIG['mintaccountid']):
                avaliable_balance = int(bank['value'])
        secondmessage = (
            "Expected balance at end of week: $%(remaining_balance)s\n"
            "Current Balance: $%(avaliable_balance)s"
        ) % {
            'remaining_balance': avaliable_balance - weektotal,
            'avaliable_balance': avaliable_balance,
        }
        message = message + secondmessage
    subject = 'Bills for the upcoming week of %(month)s %(day)s' % {
        'month': calendar.month_name[curtime.month],
        'day': stylish_date(curtime.day),
    }
    send_email(subject, message)


def stylish_date(dayofmonth):
    '''
        Takes a integer of the day of the month and returns the current postfix
        title, such as th, rd, nd
    '''
    if 4 <= dayofmonth % 100 <= 20:
        return str(dayofmonth) + "th"
    else:
        return str(dayofmonth) + {1: "st", 2: "nd", 3: "rd"}.get(
            dayofmonth % 10, "th"
        )


def main():
    '''Main'''
    with open(BILLFILE, 'r') as infile:
        do_notifications(get_notifications(yaml.load(infile)))

if __name__ == "__main__":
    main()
