from flask.ext.mail import Message
from . import mail
from flask import current_app, render_template

import smtplib
from email.mime.text import MIMEText

mailto_list=["1155065988@link.cuhk.edu.hk"]
mail_host="smtp.163.com"
mail_user="shinnqy@163.com"
mail_pass="qy1991102691"
mail_postfix="163.com"

def send_email(to, subject, template, **kwargs):
	# msg = Message(current_app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + subject, sender = current_app.config['FLASKY_MAIL_SENDER'], recipients = [0])
	msg = Message('[CUHK Exchange]' + subject, sender='CUHK Exchange Admin <Admin@cuhkexchange.com>', recipients=[to])
	msg.body = render_template(template + '.txt', **kwargs)
	msg.html = render_template(template + '.html', **kwargs)
	mail.send(msg)

def send_mail(to_list,sub,content):
    me="hello"+"<"+mail_user+"@"+mail_postfix+">"
    msg = MIMEText(content,_subtype='html',_charset='gb2312')
    msg['Subject'] = sub
    msg['From'] = me
    msg['To'] = ";".join(to_list)
    try:
        s = smtplib.SMTP()
        s.connect(mail_host)
        s.login(mail_user,mail_pass)
        s.sendmail(me, to_list, msg.as_string())
        s.close()
        return True
    except Exception, e:
        print str(e)
        return False