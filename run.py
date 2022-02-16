from swm.Chrome import Chrome
from classes.ReadInfoConf import ReadInfoConf
from classes.SendEmail import SendEmail
from classes.ReportingOfEpidemicSituation import ReportingOfEpidemicSituation
import configparser
import os

if __name__ == "__main__":
    # 读取配置
    cur_home_dir = "C:" + os.environ["HOMEPATH"]
    infoconf_dir = os.path.join(cur_home_dir, "infoconf")
    webdriverconf_dir = os.path.join(cur_home_dir, "webdriverconf")
    if not os.path.exists(infoconf_dir):
        os.mkdir(infoconf_dir)
    if not os.path.exists(webdriverconf_dir):
        os.mkdir(webdriverconf_dir)
    
    infoconf_path = os.path.abspath(os.path.join(infoconf_dir, "conf.ini"))
    webdriverconf_path = os.path.abspath(os.path.join(webdriverconf_dir, "conf.ini"))

    if not os.path.exists(infoconf_path):
        print("请现在您windows的家目录下创建 infoconf/conf.ini 文件并正确配置")
        exit(0)
    
    if not os.path.exists(webdriverconf_dir):
        print("请现在您windows的家目录下创建 webdriverconf/conf.ini 文件并正确配置")
        exit(0)
    
    # read_info_conf = ReadInfoConf(confpath="infoconf/conf.ini")
    read_info_conf = ReadInfoConf(confpath=infoconf_path)

    stu_number = read_info_conf.get('info', 'stu_number')
    stu_passwd = read_info_conf.get('info', 'stu_passwd')
    url = read_info_conf.get('info', 'url')

    # 检查conf.ini中指定的chromedriver版本和chrome版本是否匹配，不匹配则重新下载并解压
    # chrome_webdriver_setup = Chrome("webdriverconf/conf.ini")
    chrome_webdriver_setup = Chrome(webdriverconf_path)
    
    read_info_conf_webdriver = ReadInfoConf(confpath=webdriverconf_path)
    executable_path = read_info_conf_webdriver.get('driver', 'absPath')

    # 疫情填报
    reportingOfEpidemicSituation = ReportingOfEpidemicSituation(
        executable_path = executable_path, url=url, stu_number=stu_number, stu_passwd=stu_passwd)
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
