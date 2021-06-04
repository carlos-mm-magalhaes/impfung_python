#!/usr/bin/env python
# coding: utf-8

import smtplib
import pandas as pd
from string import Template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def read_template(filename):
    with open(filename, 'r', encoding='utf-8') as template_file:
        template_file_content = template_file.read()
    return Template(template_file_content)

MY_ADDRESS  = 'xxx' #gmail
MY_PASSWORD = 'xxx'

df = pd.read_csv('doctors.csv', usecols=['doctor', 'street', 'PLZ', 'email', 'url'])
df.drop_duplicates(subset=['email'], inplace=True)
df.dropna(subset=['email'], inplace=True)


smtp_object = smtplib.SMTP('smtp.gmail.com',587)
smtp_object.ehlo()
smtp_object.starttls()
smtp_object.login(MY_ADDRESS,MY_PASSWORD)

message_template = read_template('message.txt')

# For each contact, send the email:
for email in df['email']:
    msg = MIMEMultipart()       # create a message

    # add in the actual person name to the message template
    # setup the parameters of the message
    msg['From']=MY_ADDRESS
    msg['To']=email
    msg['Subject']="Anfrage auf Covid-19 Impfung"

    # add in the message body
    msg.attach(MIMEText(message_template.template, 'plain'))

    # send the message via the server set up earlier.
    smtp_object.send_message(msg)
    del msg