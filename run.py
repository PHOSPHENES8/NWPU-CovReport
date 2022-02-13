from selenium import webdriver
from send_email import send_email
import time

# 打开chrome浏览器
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(options=options) 
driver.maximize_window()
url = r'http://yqtb.nwpu.edu.cn/wx/xg/yz-mobile/index.jsp'
driver.get(url)

# 登录信息
username = driver.find_element_by_id('username')
password = driver.find_element_by_id('password')

stu_number = '学号'
stu_password = '登陆密码'
username.send_keys(stu_number)
password.send_keys(stu_password)

# 自动填报
driver.find_element_by_name('submit').click()
time.sleep(1)       # 暂停线程1s，防止部分页面跳转过慢导致运行失败
driver.find_element_by_partial_link_text('每日填报').click()
driver.find_element_by_partial_link_text('提交填报信息').click()
time.sleep(1)
driver.find_element_by_class_name('co3').click()
driver.find_element_by_partial_link_text('确认提交').click()
time.sleep(2)
driver.close()
send_email()