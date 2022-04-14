import smtplib
from email.mime.text import MIMEText
from email.header import Header
from classes.ReadInfoConf import ReadInfoConf

class SendEmail():
    """
    from_addr = 'YOUR_EMAIL@163.com'
    password  = '邮箱授权码'
    to_addr = 'YOUR_EMAIL@163.com'
    smtp_server = 'smtp.163.com'
    """

    def __init__(
        self,
        from_addr,
        password,
        to_addr,
        smtp_server
    ) -> None:

        self.from_addr = from_addr
        self.password = password
        self.to_addr = to_addr
        self.smtp_server = smtp_server

    """
    header_content = "每日疫情填报情况",
    content = "'已完成今日疫情填报表(づ￣ 3￣)づ'"
    """

    def send_email(
        self,
        header_content,
        content,
    ):

        msg = MIMEText(content, 'plain', 'utf-8')
        msg['From'] = Header(self.from_addr)
        msg['To'] = Header(self.to_addr)
        msg['Subject'] = Header(header_content)

        # 开启发信服务，这里使用的是加密传输
        server = smtplib.SMTP_SSL(self.smtp_server)
        server.connect(self.smtp_server, 465)
        server.login(self.from_addr, self.password)
        server.sendmail(self.from_addr, self.to_addr, msg.as_string())
        server.quit()


if __name__ == "__main__":
    read_info_conf = ReadInfoConf(confpath="infoconf/conf.ini")
    from_addr = read_info_conf.get('163email', 'from_addr')
    password = read_info_conf.get('163email', 'password')
    to_addr = read_info_conf.get('163email', 'to_addr')
    smtp_server = read_info_conf.get('163email', 'smtp_server')
    sendEmail = SendEmail(
        from_addr=from_addr,
        password=password,
        to_addr=to_addr,
        smtp_server=smtp_server)
    header_content = "每日疫情填报情况"
    content = "'已完成今日疫情填报表(づ￣ 3￣)づ'"
    sendEmail.send_email(header_content=header_content,
                         content=content)
