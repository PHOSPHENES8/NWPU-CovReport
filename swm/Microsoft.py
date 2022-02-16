#!/usr/bin/env python3
# coding=UTF-8
'''
Author: user
Date: 2020-12-08 11:41:29
LastEditors: user
LastEditTime: 2020-12-09 14:31:12
Descripttion: Edge instance
'''
import os
import urllib.parse
import urllib.request
from xml.etree import ElementTree

from swm import VERSION_RE, Browser_type, Manager


class Edge(Manager):
    def __init__(self, file):
        self.conf = super().get_ini(file)
        self.absPath = os.path.abspath(self.conf.get('driver', 'absPath'))
        self.url = self.conf.get('driver', 'url')
        self.check_match_Edge()
        self.chmod(self.absPath)

    def msedgedriver_version(self):
        cmd = r'{} --version'.format(self.absPath)
        output = super().shell(cmd)
        self.chmod(self.absPath)
        try:
            __v__ = VERSION_RE.findall(output.split(' ')[1])[0]
            print(f'current msedgedriver Version: \033[0;33;40m{__v__}\033[0m')
            return __v__
        except Exception as e:
            print(f'check msedgedriver failed: \033[0;31;40m{e}\033[0m')
            return 0

    def check_match_Edge(self):
        print('check Edge and msedgedriver wheather are matched')
        c_v = super().browser_version(Browser_type.MSEDGE)
        d_v = self.msedgedriver_version()
        if c_v == d_v:
            print('\033[0;32;40mEdge and msedgedriver are matched.\033[0m')
        else:
            save_d = os.path.dirname(self.absPath)
            self.get_msedgedriver(c_v, save_d)

    def get_msedgedriver(self, __v, save_d):
        match_list = []
        req = urllib.request.Request(url=self.url)
        req.add_header("User-Agent", "Mozilla/5.0")
        req.add_header('accept-encoding', 'gzip, deflate, br')
        rep = urllib.request.urlopen(req).read().decode('utf-8')
        root = ElementTree.fromstring(rep)
        Blobs = root.find('Blobs')
        for Blob in Blobs.findall('Blob'):
            name = Blob.find('Name').text
            if __v in name and self.os_type in name:
                match_list.append(Blob.find('Url').text)
        if match_list:
            if not os.path.exists(save_d):
                os.mkdir(save_d)
            super().download_file(match_list[-1], save_d)
        else:
            print(
                f"\033[0;31;40mDidn't find\033[0m. Maybe you should visit {self.url} individually to get")


if __name__ == '__main__':
    Edge('./demo/edge.ini')
    # print("\033[1;37;40m\tHello World\033[0m")
    # print("\033[0;31;40m\tHello World\033[0m")
    # print("\033[0;32;40m\tHello World\033[0m")
    # print("\033[0;33;40m\tHello World\033[0m")
    # print("\033[0;36;40m\tHello World\033[0m")
    # print("\033[0;34;40m\tHello World\033[0m")
