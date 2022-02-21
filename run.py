from swm.Chrome import Chrome
from classes.ReadInfoConf import ReadInfoConf
from classes.SendEmail import SendEmail
from classes.ReportingOfEpidemicSituation import ReportingOfEpidemicSituation
import configparser
import os
import platform

if __name__ == "__main__":
    # 读取配置
    cur_os = "Windows"
    if(platform.system()=='Windows'):
        cur_os = "Windows"
        try:
            cur_home_dir = "C:" + os.environ["HOMEPATH"]
        except KeyError as e:
            print(e)
            exit('找不到os.environ["HOMEPATH"]')
    elif(platform.system()=='Linux'):
        cur_os = "Linux"
        try:
            cur_home_dir = os.environ["HOME"]
        except KeyError as e:
            print(e)
            exit('找不到os.environ["HOME"]')
    else:
        cur_os = "Linux"
        try:
            cur_home_dir = os.environ["HOME"]
        except KeyError as e:
            print(e)
            exit('找不到os.environ["HOME"]')

    cur_home_dir = os.path.abspath(cur_home_dir) 
    print("当前配置文件所在文件夹为: {}.".format(cur_home_dir))

    studentinfoconf_dir = os.path.abspath(os.path.join(cur_home_dir, ".studentinfoconf"))
    webdriverconf_dir = os.path.abspath(os.path.join(cur_home_dir, ".webdriverconf"))

    file_name = os.path.join(studentinfoconf_dir, "conf.ini")
    if not os.path.exists(file_name):
        if not os.path.exists(studentinfoconf_dir):
            os.mkdir(studentinfoconf_dir)
        with open(file_name,'w',encoding='utf-8'):
            pass
        print("请先在您的家目录下创建 .infoconf/conf.ini 文件并正确配置")
        exit(1)
    
    file_name = os.path.join(webdriverconf_dir, "conf.ini")
    if not os.path.exists(file_name):
        if not os.path.exists(webdriverconf_dir):
            os.mkdir(webdriverconf_dir)
        with open(file_name,'w',encoding='utf-8'):
            pass
        print("请先在您的家目录下创建 .webdriverconf/conf.ini 文件并正确配置")
        exit(1)
    
    infoconf_path = os.path.abspath(os.path.join(studentinfoconf_dir, "conf.ini"))
    webdriverconf_path = os.path.abspath(os.path.join(webdriverconf_dir, "conf.ini"))
    
    # read_info_conf = ReadInfoConf(confpath="infoconf/conf.ini")
    read_info_conf = ReadInfoConf(confpath=infoconf_path)

    try:
        stu_number = read_info_conf.get('info', 'stu_number')
        stu_passwd = read_info_conf.get('info', 'stu_passwd')
        url = read_info_conf.get('info', 'url')
    except configparser.NoSectionError:
        print("请先在您的家目录下创建 .webdriverconf/conf.ini 文件并正确配置")
        exit(1)

    # 检查conf.ini中指定的chromedriver版本和chrome版本是否匹配，不匹配则重新下载并解压
    # chrome_webdriver_setup = Chrome("webdriverconf/conf.ini")
    if cur_os == "Windows":
        chrome_webdriver_setup = Chrome(webdriverconf_path)
    elif cur_os == "Linux":
        chrome_webdriver_setup = Chrome(webdriverconf_path)
        pass
    else:
        chrome_webdriver_setup = Chrome(webdriverconf_path)
        pass

    read_info_conf_webdriver = ReadInfoConf(confpath=webdriverconf_path)
    try:
        executable_path = read_info_conf_webdriver.get('driver', 'absPath')
    except configparser.NoSectionError:
        print("请先在您的家目录下创建 .webdriverconf/conf.ini 文件并正确配置")
        exit(1)

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
