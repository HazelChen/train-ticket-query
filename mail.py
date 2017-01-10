#-*- coding:utf-8 -*-
from email.header import Header
from email.mime.text import MIMEText
import smtplib

from_addr = ''  #发送邮箱
from_password = ''  #发送邮箱密码
smtp_server = 'smtp.qq.com' #服务器
to_addr = '' #接收邮箱

def email(input_msg):
    msg = MIMEText(str(input_msg), 'plain', 'utf-8')
    msg['From'] = '你猜我是谁'
    msg['To'] = to_addr
    msg['Subject'] = Header('[12306查查查]有消息啦', 'utf-8').encode()

    server = smtplib.SMTP_SSL(smtp_server, 465)  #smtp模式和接口
    server.set_debuglevel(1)
    server.login(from_addr, from_password)
    server.sendmail(from_addr, [to_addr], msg.as_string())
    server.quit()

    logging.info('mail sended.')