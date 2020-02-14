#!/usr/bin/python3

import sys
import base64
import smtplib
import json
import argparse
import ntpath
from getpass import getpass
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

def main():
    description = """
    Send email(s). Add additionnal -file tags to send several attachments.
    -user, -pwd, -smtp and -port flags are optionnal if a config file exists"""
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-user', help='username@domain.com')
    parser.add_argument('-pwd', help='password')
    parser.add_argument('-smtp', help='SMTP')
    parser.add_argument('-port', help='port')
    parser.add_argument('-to', metavar='adr1;adr2 ...', help='recipient adresses')
    parser.add_argument('-subject', help='subject')
    parser.add_argument('-body', help='body')
    parser.add_argument('-config', action="store_true", help='create JSON config file containing auth infos')
    parser.add_argument('-file', action='append', metavar='PATH', help='attachment')
    args = parser.parse_args()

    if len(sys.argv) < 2:
        parser.print_help()

    if args.config:
        config()

    if (args.to is not None) and (args.subject is not None):
        if (args.user and args.pwd and args.smtp and args.port) is not None:
            user = args.user
            pwd = args.pwd
            smtp = args.smtp
            port = args.port
        else:
            try:
                user, pwd, smtp, port = get_auth_from_file(sys.path[0] + "/config.json")
            except:
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
    server.ehlo()
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

def config():
    user = input("email address: ")
    password = getpass("password: ")
    smtp = input("SMTP: ")
    port = input("port: ")

    with open(sys.path[0] + "/config.json", mode="w", encoding="utf-8") as conf:
        conf.write(json.dumps({
            "user": user,
            "password": password,
            "smtp": smtp,
            "port": port 
        }))
    print(sys.path[0] + "/config.json")

if __name__ == '__main__':
    main()
