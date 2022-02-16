# 西工大疫情填报

## Setup

1. 安装所需依赖.
    
    ```shell
    git clone git@github.com:PHOSPHENES8/NWPU-CovReport.git
    cd NWPU-CovReport
    pip install requirements.txt
    ```
2. 开启stmp服务：不同邮箱开启方式不同，可自行百度
   
3. 修改配置文件
   
   配置文件有两个.
   
   一个是放在`C:\Users\Heyoungsen\infoconf\`文件夹下的`conf.ini`文件(没有自行创建)：
   > 添加两个section
    ```ini
    [info]
    stu_number=你的翱翔门户学号
    stu_passwd=你的翱翔门户密码
    url = http://yqtb.nwpu.edu.cn/wx/xg/yz-mobile/index.jsp
    
    [163email]
    from_addr = 你的163邮箱
    password  = 你的163 smtp/pop3 密码
    to_addr = 你要给哪个邮箱发邮件
    smtp_server = smtp.163.com
    ```
    > 例如改成如下:
    ```ini
    [info]
    stu_number=8888888888
    stu_passwd=cym8888888
    url = http://yqtb.nwpu.edu.cn/wx/xg/yz-mobile/index.jsp

    [163email]
    from_addr = 8888888888@163.com
    password  = TSAAUDYNABCDEFGH
    to_addr = 8888888888@foxmail.com
    smtp_server = smtp.163.com
    ```

    一个是放在`C:\Users\Heyoungsen\webdriverconf\`文件夹下的`conf.ini`文件(没有自行创建)：
    > 添加一个section
    ```ini
    [driver]
    # please input abs/relative path you chromedriver is.
    # current path is directory where README.md is.
    absPath=你希望把chromedriver存在哪里，可以写绝对路径，可以写相对路径，写相对路径的话，当前路径为该项目根目录。
    ; url=http://npm.taobao.org/mirrors/chromedriver
    url=https://chromedriver.storage.googleapis.com
    ```
    > 例如如下:
    ```ini
    [driver]
    # please input abs/relative path you chromedriver is.
    # current path is directory where README.md is.
    absPath=chromedriver/chromedriver.exe
    ; url=http://npm.taobao.org/mirrors/chromedriver
    url=https://chromedriver.storage.googleapis.com
    ```

4. 定时执行

- 通过控制面板→计划任务→创建基本任务→填写相应内容→完成
- 增加任务指令
  
    ```shell
    cd 当前项目目录
    python run.py
    ```

## Notes

- 因为西工大会自动记录上一天的信息，所以不需要填报其他信息可直接提交；

- 若修改相应信息，参见下方：

  ```python
  #如果需要更改一些内容可参考以下代码
  # 近15天是否前往或经停过武汉市、湖北省，或其他有病例报告的社区？
  driver.find_element_by_xpath('//*[@id="rbxx_div"]/div[6]/label[3]').click()
  driver.find_element_by_xpath('//*[@id="sfjthb_ms"]').clear()
  driver.find_element_by_xpath('//*[@id="sfjthb_ms"]').send_keys('人在湖北')
  
  # 近15天接触过出入或居住在武汉市、湖北省的人员，以及其它有病例社区的发热或呼吸道症状患者？
  driver.find_element_by_xpath('//*[@id="rbxx_div"]/div[8]/label[3]').click()
  driver.find_element_by_xpath('//*[@id="hbjry_ms"]').clear()
  driver.find_element_by_xpath('//*[@id="hbjry_ms"]').send_keys('人在湖北')
  
  # 近15天您或家属是否接触过疑似或确诊患者，或无症状感染患者（核酸检测阳性者）？
  driver.find_element_by_xpath('//*[@id="rbxx_div"]/div[10]/label[1]').click()
  ```

## Reference

- https://www.freesion.com/article/6211985604/
- [检测注册表去比对chromedriver版本和chrome版本是否符合](https://gitee.com/z417/selenium-webdriver-manager)