#coding:utf-8
from config import  SMTP_HOST, SMTP_USERNAME, SMTP_PASSWORD

from email.MIMEText import MIMEText
from email.Header import Header
from email.Utils import formataddr
import smtplib



SENDER_NAME=SMTP_USERNAME
SENDER_MAIL=SMTP_HOST

NOT_SUPPORT_UTF8_DOMAIN = set(['tom.com', 'hotmail.com', 'msn.com', 'yahoo.com'])

def ignore_encode(s, enc):
    return s.decode('utf-8', 'ignore').encode(enc, 'ignore')



def sendmail_imp(
        smtp,
        sender, sender_name,
        recipient, recipient_name,
        subject, body, enc='utf-8',
        format='plain'
    ):
    if not subject:
        return

    at = recipient.find('@')
    if at <= 0:
        return

    domain = recipient[at+1:].strip()
    if domain not in NOT_SUPPORT_UTF8_DOMAIN:
        enc = 'utf-8'
    else:
        enc = 'gb18030'

    if enc.lower() != 'utf-8':
        sender_name = ignore_encode(sender_name, enc)
        recipient_name = ignore_encode(recipient_name, enc)
        body = ignore_encode(body, enc)
        subject = ignore_encode(subject, enc)

    msg = MIMEText(body, format, enc)
    msg['Subject'] = Header(subject, enc)

    sender_name = str(Header(sender_name, enc))
    msg['From'] = formataddr((sender_name, sender))

    recipient_name = str(Header(recipient_name, enc))
    msg['To'] = formataddr((recipient_name, recipient))

    smtp.sendmail(sender, recipient, msg.as_string())


def sendmail(
    subject,
    text, email, name=None, sender=SENDER_MAIL,
    sender_name=SENDER_NAME,
    format='plain'
):
    server = smtplib.SMTP(SMTP_HOST)
    server.ehlo()
    server.login(SMTP_USERNAME, SMTP_PASSWORD)

    #print email
    if type(text) is unicode:
        text = text.encode("utf-8","ignore") 
    if type(subject) is unicode:
        subject = subject.encode("utf-8","ignore")
    sendmail_imp(server, sender, sender_name, email, name, subject, text, format=format)
    server.quit()


if '__main__' == __name__:
    from time import time
    sendmail('time %s'%time(), u'感谢教主贡献代码', '412618768@qq.com')
    print SENDER_MAIL
