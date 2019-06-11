#-*- coding: UTF-8 -*- 
from email.mime.text import MIMEText
from email.header import Header
from email.utils import parseaddr, formataddr
from smtplib import SMTP_SSL
import json

def load_config():
    f = open('config.json', 'r')
    #print(f.read())
    config = f.read()
    config_json = json.loads(config)
    global EMAIL_USER
    EMAIL_USER = config_json["sender"]
    global EMAIL_REVEIVER
    receiver_str = str(config_json["receiver"])
    EMAIL_REVEIVER = receiver_str.split(',')
    global SMTP_SERVER
    SMTP_SERVER = config_json["server"]
    global SMTP_PASSWORD
    SMTP_PASSWORD = config_json["password"]

def __format_addr(address):
    """用户信息和邮件解析函数"""
    re, addr = parseaddr(address)
    # 返回编码解析后的数据
    return formataddr((Header(re, 'utf-8').encode(),addr))
 
def send_msg(content):
    load_config()
    message = MIMEText('<h1>{}</h1>'.format(content), 'html', 'utf-8')
    message['from'] = __format_addr('lifeng <{}>'.format(EMAIL_USER))
    message['to'] = __format_addr('lk <{}>'.format(EMAIL_REVEIVER))
    message['subject'] = '每日博客汇总' #邮件主题
    # 连接邮箱服务器
    mail_server = SMTP_SSL(SMTP_SERVER, 465)
    mail_server.set_debuglevel(1)
     
    # 登录服务器
    mail_server.login(EMAIL_USER, SMTP_PASSWORD)
     
    # 发送邮件
    mail_server.sendmail(from_addr=EMAIL_USER, to_addrs=EMAIL_REVEIVER, msg=message.as_string())
     
    # 关闭并退出客户端
    mail_server.quit()
    print('邮件已发送>>>>')

if __name__ == '__main__':
    send_msg("邮件内容")