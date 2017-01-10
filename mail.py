#-*- coding:utf-8 -*-
from email.header import Header
from email.mime.text import MIMEText
import smtplib

from_addr = ''  #发送邮箱
password = ''  #接收邮箱
smtp_server = 'smtp.qq.com' #服务器
to_addr = ''

def email(trip):

    # 普通列车
    msg = MIMEText(str(trip), 'plain', 'utf-8')
    msg['From'] = '你猜我是谁'
    msg['To'] = to_addr
    msg['Subject'] = Header('有票啦', 'utf-8').encode()

    server = smtplib.SMTP_SSL(smtp_server, 465)  #smtp模式和接口
    server.set_debuglevel(1)
    server.login(from_addr, password)
    server.sendmail(from_addr, [to_addr], msg.as_string())
    server.quit()

    print('发送邮件成功')