from flask.ext.mail import Message
from . import mail
from flask import current_app, render_template

import smtplib
# from email.mime.text import MIMEText

FROMADDR = "shinnqy@gmail.com"
LOGIN    = FROMADDR
PASSWORD = "qy1991102691"
# TOADDRS  = ["my.real.address@gmail.com"]
# SUBJECT  = "Test"

def send_email(to, subject, template, **kwargs):
	# msg = Message(current_app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + subject, sender = current_app.config['FLASKY_MAIL_SENDER'], recipients = [0])
	msg = Message('[CUHK Exchange]' + subject, sender='CUHK Exchange Admin <Admin@cuhkexchange.com>', recipients=[to])
	msg.body = render_template(template + '.txt', **kwargs)
	msg.html = render_template(template + '.html', **kwargs)
	mail.send(msg)

def send_mail(to_list, sub, content):
	msg = ("From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n"  % (FROMADDR, ", ".join(to_list), sub))
	msg += "some text\r\n%s" % (content)
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.set_debuglevel(1)
	server.ehlo()
	server.starttls()
	server.login(LOGIN, PASSWORD)
	server.sendmail(FROMADDR, to_list, msg)
	server.quit()