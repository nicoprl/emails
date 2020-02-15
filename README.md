# emails.py

Simple Python CLI to send emails.

## Prerequisites

Python 3.x

## Installing

`wget https://raw.githubusercontent.com/nicoprl/emails/master/emails.py`

## Usage
```
usage: emails.py [-h] [-user USER] [-pwd PWD] [-smtp SMTP] [-port PORT]
                 [-to adr1;adr2 ...] [-subject SUBJECT] [-body BODY] [-config]
                 [-file PATH]

Send email(s). Add additionnal -file tags to send several attachments. -user,
-pwd, -smtp and -port flags are optionnal if a config file exists. To create a
config file, type emails.py -config

optional arguments:
  -h, --help         show this help message and exit
  -user USER         username@domain.com
  -pwd PWD           password
  -smtp SMTP         SMTP
  -port PORT         port
  -to adr1;adr2 ...  recipient adresses
  -subject SUBJECT   subject
  -body BODY         body
  -config            create JSON config file containing auth infos
  -file PATH         attachment
```
## Exemples

#### With config file

`emails.py -to "bob@domain.com;john@domain.com" -subject "This is the title" -body "email body"`

#### Without config file

`emails.py -user "alice@domain.com" -pwd "123456" -smtp "smtp.gmail.com" -port 587 -to "bob@domain.com;john@domain.com" -subject "This is the title" -body "email body" -file "./cat.jpeg" -file "./snoopy.jpeg"`

## Configuration file exemple
```json
{
  "user": "alice@domain.com",
  "password": "123456",
  "smtp": "smtp.gmail.com",
  "port": 587
}
```
