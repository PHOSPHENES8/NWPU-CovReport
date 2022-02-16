from selenium import webdriver


class ReportingOfEpidemicSituation():
    def __init__(self, url, stu_number, stu_passwd) -> None:
        self.url = url
        self.stu_number = stu_number
        self.stu_passwd = stu_passwd

        self.time_out = 20
        self.options = webdriver.ChromeOptions()
        self.options.add_experimental_option(
            'excludeSwitches', ['enable-logging'])
        self.options.add_argument('--headless')
        self.driver = webdriver.Chrome(options=self.options)

    def run(self):
        # self.driver.maximize_window()

        self.driver.get(self.url)

        username = self.driver.find_element_by_id('username')
        passwd = self.driver.find_element_by_id('password')
        username.send_keys(self.stu_number)
        passwd.send_keys(self.stu_passwd)

        # 自动填报
        self.driver.find_element_by_name('submit').click()
        self.driver.implicitly_wait(self.time_out)
        self.driver.find_element_by_partial_link_text('每日填报').click()
        self.driver.implicitly_wait(self.time_out)
        self.driver.find_element_by_partial_link_text('提交填报信息').click()
        self.driver.implicitly_wait(self.time_out)
        self.driver.find_element_by_class_name('co3').click()
        self.driver.implicitly_wait(self.time_out)
        self.driver.find_element_by_partial_link_text('确认提交').click()
        self.driver.implicitly_wait(self.time_out)
        self.driver.close()
