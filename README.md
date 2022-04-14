# 西工大疫情填报

## Setup

1. 安装所需依赖.
    
    ```shell
    cd NWPU-CovReport
    pip install -r requirements.txt
    ```
2. 开启stmp服务：不同邮箱开启方式不同，可自行百度

## Windows用户

1. 配置

    修改配置文件, 配置文件有两个.
      
    一个是放在`C:\Users\您的用户名称\.infoconf\`文件夹下的`conf.ini`文件(没有自行创建)：

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

    一个是放在`C:\Users\您的用户名称\.webdriverconf\`文件夹下的`conf.ini`文件(没有自行创建)：

    > 添加一个section

    ```ini
    [driver]
    absPath=你希望把chromedriver存在哪里，写绝对路径
    ; url=http://npm.taobao.org/mirrors/chromedriver
    url=https://chromedriver.storage.googleapis.com
    ```

    > 例如如下:

    ```ini
    [driver]
    absPath=D:/Source/chromedriver/chromedriver.exe
    ; url=http://npm.taobao.org/mirrors/chromedriver
    url=https://chromedriver.storage.googleapis.com
    ```

    **注意：absPath=D:/Source/chromedriver/chromedriver.exe，最后的chromedriver.exe要加上，代表chromedriver.exe这个文件**

2. 打包

* 因为使用到了本地的python类包，和相对路径有关，故需要打包。
* pyinstaller -F run.py
* 文件夹dist下就是可执行exe

3. 定时执行

- 通过控制面板→计划任务→创建基本任务→填写相应内容→完成

## Linux用户

1. 配置

    修改配置文件, 配置文件有两个.
      
    一个是放在`/home/您的用户名称/.infoconf/`文件夹下的`conf.ini`文件(没有自行创建)：

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

    一个是放在`/home/您的用户名称/.webdriverconf/`文件夹下的`conf.ini`文件(没有自行创建)：

    > 添加一个section
    ```ini
    [driver]
    absPath=你希望把chromedriver存在哪里，写绝对路径
    ; url=http://npm.taobao.org/mirrors/chromedriver
    url=https://chromedriver.storage.googleapis.com
    ```

    > 例如如下:

    ```ini
    [driver]
    absPath=/home/hiyoungshen/packege/chromedriver
    ; url=http://npm.taobao.org/mirrors/chromedriver
    url=https://chromedriver.storage.googleapis.com
    ```

    **注意：absPath=D:/Source/chromedriver/chromedriver，最后的chromedriver要加上，代表chromedriver这个文件**

2. 打包(不一定需要)

* 因为使用到了本地的python类包，和相对路径有关，故需要打包。
* pyinstaller -F run.py
* 文件夹dist下就是可执行文件

3. 定时执行

* linux脚本定时执行例如
  ```shell
  sudo crontab -e 进入编辑模式
  增加一行:
  59 11 1 * * /home/hiyoungshen/source/NWPU-CovReport/run.sh
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