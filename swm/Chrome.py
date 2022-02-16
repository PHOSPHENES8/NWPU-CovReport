#!/usr/bin/env python3
# coding=UTF-8
'''
Author: user
Date: 2020-12-08 11:41:29
LastEditors: user
LastEditTime: 2020-12-09 10:41:03
Descripttion: chrome instance
'''
import os
import re
import urllib.parse
import urllib.request
from xml.etree import ElementTree

from swm import VERSION_RE, Browser_type, Manager


class Chrome(Manager):
    def __init__(self, file):
        self.conf = super().get_ini(file)
        self.absPath = os.path.abspath(self.conf.get('driver', 'absPath'))
        self.url = self.conf.get('driver', 'url')
        self.check_match_chrome()
        self.chmod(self.absPath)

    def chromedriver_version(self):
        cmd = r'{} --version'.format(self.absPath)
        output = super().shell(cmd)
        self.chmod(self.absPath)
        try:
            __v__ = VERSION_RE.findall(output.split(' ')[1])[0]
            print(f'current chromedriver Version: \033[0;33;40m{__v__}\033[0m')
            return __v__
        except Exception as e:
            print(f'check chromedriver failed: \033[0;31;40m{e}\033[0m')
            return 0

    def check_match_chrome(self):
        print('check Chrome and chromedriver wheather are matched')
        c_v = super().browser_version(Browser_type.GOOGLE)
        d_v = self.chromedriver_version()
        if c_v == d_v:
            print('\033[0;32;40mChrome and chromedriver are matched.\033[0m')
        else:
            save_d = os.path.dirname(self.absPath)
            self.get_chromedriver(c_v, save_d)

    def get_chromedriver(self, __v, save_d):
        match_list = []
        ot = 'win32' if 'win' in self.os_type else self.os_type
        if 'taobao' in self.url:
            rep = urllib.request.urlopen(self.url).read().decode('utf-8')
            # http://npm.taobao.org/mirrors/chromedriver/83.0.4103.39/chromedriver_win32.zip
            # '<a href="/mirrors/chromedriver/84.0.4147.30/">84.0.4147.30/</a>'
            directory = re.compile(r'>(\d.*?/)</a>').findall(rep)
            for i in directory:
                if __v in i:
                    match_list.append(i)
            dir_uri = urllib.parse.urljoin(f'{self.url}/', match_list[-1])
            driver_name = f'chromedriver_{ot}.zip'
            down_uri = urllib.parse.urljoin(dir_uri, driver_name)
        else:
            rep = urllib.request.urlopen(self.url).read().decode('utf-8')
            root = ElementTree.fromstring(rep)
            xmlns = '{http://doc.s3.amazonaws.com/2006-03-01}'
            for child in root.findall(xmlns + 'Contents'):
                key = child.find(xmlns + 'Key').text
                if __v in key and 'chromedriver' in key:
                    if ot in key:
                        match_list.append(key)
            driver_name = match_list[-1]
            down_uri = urllib.parse.urljoin(self.url, driver_name)
        if not os.path.exists(save_d):
            os.mkdir(save_d)
        super().download_file(down_uri, save_d)


if __name__ == '__main__':
    c = Chrome('./demo/conf.ini')
    # print("\033[1;37;40m\tHello World\033[0m")
    # print("\033[0;31;40m\tHello World\033[0m")
    # print("\033[0;32;40m\tHello World\033[0m")
    # print("\033[0;33;40m\tHello World\033[0m")
    # print("\033[0;36;40m\tHello World\033[0m")
    # print("\033[0;34;40m\tHello World\033[0m")
