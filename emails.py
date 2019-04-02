#!/usr/bin/python3

import sys
import smtplib
import argparse
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

def main():
    parser = argparse.ArgumentParser(description='Send email. Add additionnal -file tags to send several attachments')
    parser.add_argument('-user', help='username@domain.com')
    parser.add_argument('-pwd', help='password')
    parser.add_argument('-smtp', help='SMTP')
    parser.add_argument('-port', help='port')
    parser.add_argument('-to', metavar='adr1;adr2 ...', help='recipient adresses')
    parser.add_argument('-subject', help='subject')
    parser.add_argument('-body', help='body')
    parser.add_argument('-file', action='append', metavar='NAME:PATH', help='attachment')
    args = parser.parse_args()
    
    try:
        for recipient in args.to.split(';'):
            sendEmail(args.user, args.pwd, args.smtp, args.port, recipient, args.subject, args.body, args.file)
    except Exception as e:
        print(e)
        sys.exit(1)
    else:
        print('email(s) sent')

def sendEmail(user, pwd, smtp, port, to, subject, text, attachment=[]):
    msg = MIMEMultipart()
    msg["Subject"] = subject
    msg["From"] = user
    msg["To"] = to

    msg.attach(MIMEText(text, 'plain'))

    if attachment:
        for e in attachment:
            with open(e.split(':')[1], 'rb') as f:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(f.read())
                encoders.encode_base64(part)
                part.add_header(
                    'Content-Disposition', 
                    'attachment; filename = {0}'.format(e.split(':')[0])
                )
                msg.attach(part)

    server = smtplib.SMTP(smtp, port)
    server.ehlo()
    server.starttls()
    server.login(user, pwd)
    txt = msg.as_string()
    server.sendmail(user, to, txt)
    server.close()

if __name__ == '__main__':
    main()
