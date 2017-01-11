#-*- coding:utf-8 -*-
from email.header import Header
from email.mime.text import MIMEText
import smtplib
import config, logging

def email(input_msg):
    msg = MIMEText(str(input_msg), 'plain', 'utf-8')
    msg['From'] = '你猜我是谁'
    msg['To'] = config.mail_to_addr
    msg['Subject'] = Header('[12306查查查]有消息啦', 'utf-8').encode()

    server = smtplib.SMTP_SSL(config.mail_smtp_server, 465)  #smtp模式和接口
    server.set_debuglevel(1)
    server.login(config.mail_from_addr, config.mail_from_password)
    server.sendmail(config.mail_from_addr, [config.mail_to_addr], msg.as_string())
    server.quit()

    logging.info('mail sended.')