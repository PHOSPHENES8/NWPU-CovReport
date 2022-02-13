import smtplib
from email.mime.text import MIMEText
from email.header import Header

def send_email():
    from_addr = 'YOUR_EMAIL@163.com'
    password  = '邮箱授权码'
    to_addr = 'YOUR_EMAIL@163.com'
    smtp_server = 'smtp.163.com'

    msg = MIMEText('已完成今日疫情填报表(づ￣ 3￣)づ', 'plain', 'utf-8')
    msg['From'] = Header(from_addr)
    msg['To'] = Header(to_addr)
    msg['Subject'] = Header('每日疫情填报情况')

    # 开启发信服务，这里使用的是加密传输
    server = smtplib.SMTP_SSL(smtp_server)
    server.connect(smtp_server, 465)
    server.login(from_addr, password)
    server.sendmail(from_addr, to_addr, msg.as_string())
    server.quit()