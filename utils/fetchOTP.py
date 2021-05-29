import datetime
import imaplib
import email
import traceback
from email.header import decode_header
# -------------------------------------------------
#
# Utility to read email from Gmail Using Python
#
# ------------------------------------------------
import time
from email import utils

import pytz

SMTP_SERVER = "imap.gmail.com"
SMTP_PORT = 993

def read_email_from_gmail(receivedAfter, username, password):
    try:
        mail = imaplib.IMAP4_SSL(SMTP_SERVER)
        mail.login(username, password)

        otps = []
        count = 0
        while otps.__len__() == 0:
            mail.select('inbox')
            typ, mail_ids = mail.search(None, '(ALL SUBJECT "%s")' % "Message from SMS Forwarder")

            id_list = mail_ids[0].split()
            if len(id_list) != 0:
                num = id_list[len(id_list)-1]
                typ, msg_data = mail.fetch(num, '(RFC822)')
                #for response_part in msg_data:
                msg = email.message_from_bytes(msg_data[0][1])
                received = decode_header(msg["Date"])[0][0]
                body = ''
                if msg.is_multipart():
                    for payload in msg.get_payload():
                        body = str(payload.get_payload(True))
                else:
                    body = msg.get_payload()

                receivedOn = parseDate(received)
                otp = parsebody(body)

                if receivedOn > receivedAfter:
                    otps.append(otp)
            time.sleep(1)
            count = count + 1
            if count > 120:
                return ''

        return otps[0]

    except Exception as e:
        traceback.print_exc()
        print(str(e))


def parseDate(rawdate):
    date = utils.parsedate_to_datetime(rawdate)
    return date

def parsebody(body):
    start = body.find("Your OTP to register/access CoWIN is ") + len("Your OTP to register/access CoWIN is ")
    end = body.find(". It will be valid for 3 minutes. - CoWIN")
    otp = body[start:end]
    return otp

def fetchOTP(time, username, password):
    return read_email_from_gmail(time, username, password)

#yfetchOTP(datetime.datetime.now(pytz.utc), "anandsaha321@gmail.com", "#include<1987>")
