import imp
from swm.Chrome import Chrome
from classes.ReadInfoConf import ReadInfoConf
from classes.SendEmail import SendEmail
from classes.ReportingOfEpidemicSituation import ReportingOfEpidemicSituation
import configparser


if __name__ == "__main__":
    # 读取配置
    read_info_conf = ReadInfoConf(confpath="infoconf/conf.ini")

    stu_number = read_info_conf.get('info', 'stu_number')
    stu_passwd = read_info_conf.get('info', 'stu_passwd')
    url = read_info_conf.get('info', 'url')

    # 检查conf.ini中指定的chromedriver版本和chrome版本是否匹配，不匹配则重新下载并解压
    chrome_webdriver_setup = Chrome("webdriverconf/conf.ini")

    # 疫情填报
    reportingOfEpidemicSituation = ReportingOfEpidemicSituation(
        url=url, stu_number=stu_number, stu_passwd=stu_passwd)
    reportingOfEpidemicSituation.run()

    try:
        from_addr = read_info_conf.get('163email', 'from_addr')
        password = read_info_conf.get('163email', 'password')
        to_addr = read_info_conf.get('163email', 'to_addr')
        smtp_server = read_info_conf.get('163email', 'smtp_server')

        # 发送邮件提醒
        sendEmail = SendEmail(
            from_addr=from_addr,
            password=password,
            to_addr=to_addr,
            smtp_server=smtp_server)
        header_content = "每日疫情填报情况"
        content = "'已完成今日疫情填报表(づ￣ 3￣)づ'"
        sendEmail.send_email(header_content=header_content,
                             content=content)
    except configparser.NoSectionError:
        pass
