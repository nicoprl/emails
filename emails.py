#!/usr/bin/python3

import sys
import base64
import smtplib
import json
import argparse
import ntpath
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

def main():
    description = """
    Send email(s). Add additionnal -file tags to send several attachments.
    -user, -pwd, -smtp and -port flags are optionnal if --config CONFIG is provided
    config file must be a json file containing: user, password, smtp, port"""
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-user', required=False, help='username@domain.com')
    parser.add_argument('-pwd', required=False, help='password')
    parser.add_argument('-smtp', required=False, help='SMTP')
    parser.add_argument('-port', required=False, help='port')
    parser.add_argument('-to', required=True, metavar='adr1;adr2 ...', help='recipient adresses')
    parser.add_argument('-subject', required=True, help='subject')
    parser.add_argument('-body', required=False, help='body')
    parser.add_argument('--config', required=False, help='JSON config file containing auth infos')
    parser.add_argument('-file', action='append', metavar='PATH', help='attachment')
    args = parser.parse_args()

    if args.config is not None:
        user, pwd, smtp, port = get_auth_from_file(args.config)
    elif (args.user and args.pwd and args.smtp and args.port) is not None:
        user = args.user
        pwd = args.pwd
        smtp = args.smtp
        port = args.port
    else:
        print('ERROR: provide -user, -pwd, -smtp and -port if --config is missing')
        sys.exit(1)

    if args.body is None:
        body = ''
    else:
        body = args.body
    
    for recipient in args.to.split(';'):
        try:
            sendEmail(user, pwd, smtp, port, recipient, args.subject, body, args.file)
        except Exception as e:
            print(e)
            sys.exit(1)
        else:
            print("done.")

def sendEmail(user, pwd, smtp, port, to, subject, text, attachment=[]):
    msg = MIMEMultipart()
    msg["Subject"] = subject
    msg["From"] = user
    msg["To"] = to

    msg.attach(MIMEText(text, 'plain'))

    if attachment:
        for e in attachment:
            with open(e, 'rb') as f:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(f.read())
                encoders.encode_base64(part)
                part.add_header(
                    'Content-Disposition', 
                    'attachment; filename = {0}'.format(ntpath.basename(e))
                )
                msg.attach(part)

    server = smtplib.SMTP(smtp, port)
    server.ehlo()
    server.starttls()
    server.login(user, pwd)
    txt = msg.as_string()
    server.sendmail(user, to, txt)
    server.close()

def get_auth_from_file(jsonFile):
    try:
        with open(jsonFile) as configFile:
            config = json.load(configFile)
            return config["user"], config["password"], config["smtp"], config["port"]
    except Exception as e:
        print(e)
        sys.exit(1)

if __name__ == '__main__':
    main()
