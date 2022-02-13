### 西工大疫情填报

#### 0. Setup

- chrome驱动：[下载链接](https://liushilive.github.io/github_selenium_drivers/md/Chrome.html)（需要将解压后的exe文件放置到chrome安装文件夹中，本仓库中的exe文件对应chrome98版本）
- Python库：selenium
- 开启stmp服务：不同邮箱开启方式不同，可自行百度

#### 1. Execute

- 自动疫情填报执行：`python run.py`
- 取消发送邮件提醒：去掉最后一行注释`send_email()`
- 通过控制面板→计划任务→创建基本任务→填写相应内容→完成

#### 2. Notes

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

#### 3. Reference

- https://www.freesion.com/article/6211985604/