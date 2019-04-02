Simple Python CLI to send emails 

# Prerequisites

Python 3.x

# Installing

`wget https://raw.githubusercontent.com/nicoprl/emails/master/emails.py`

# Usage
```
usage: emails.py [-h] [-user USER] [-pwd PWD] [-smtp SMTP] [-port PORT]
                 [-to adr1;adr2 ...] [-subject SUBJECT] [-body BODY]
                 [-file NAME:PATH]

Send email. Add additionnal -file tags to send several attachments

  -h, --help         show this help message and exit
  -user USER         username@domain.com
  -pwd PWD           password
  -smtp SMTP         SMTP
  -port PORT         port
  -to adr1;adr2 ...  recipient adresses
  -subject SUBJECT   subject
  -body BODY         body
  -file NAME:PATH    attachment
```
# Exemple

`emails.py -user "alice@domain.com" -pwd "123456" -smtp "smtp.gmail.com" -port 587 -to "bob@domain.com;john@domain.com" -subject "This is the title" -body "email body" -file "img1.jpeg:./cat.jpeg" -file "img2.jpeg:./snoopy.jpeg"`