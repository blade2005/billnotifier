# billnotifier

Purpose: Populate yaml file in ~/.config/bill_notify/bills.yaml.conf and a config file for sending email and logging into mint in ~/.config/bill_notify/email.conf

####  ~/.config/bill_notify/bills.yaml.conf
```
- amount: 600
  description: Rent
  duedate: 1
  name: Landlord
```

####  ~/.config/bill_notify/config.conf
```
[billnotify]
host = smtp.domain.com
username = username@domain.com
password = password
port = 25
ssl = 0
auth = 0
from = username@domain.com
to = email1@domain.com,email2@domain2.com
mintuser = mintusername@domain.com
mintpassword = mintpassword
mintaccountid = mint_account_id
```

You can get the mint account id from running mintapi from the commandline and looking through the output for the account you want. Alternatively you can run accountprint.py after setting up your config file

Also you will want to modify the source code slightly to update what day you want to be emailed. This is on line 23