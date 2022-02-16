#!/usr/bin/env python3
# coding=UTF-8
'''
Author: user
Date: 2020-12-08 11:40:07
LastEditors: user
LastEditTime: 2020-12-09 14:12:37
Descripttion: package
'''
import os
import re
import subprocess
import sys
import tarfile
import urllib.request
import zipfile
from configparser import RawConfigParser
from enum import Enum
from urllib.error import ContentTooShortError

VERSION_RE = re.compile(r'\d+\.\d+\.\d+')


class OS_type(Enum):
    LINUX = 'linux'
    MAC = 'mac'
    WIN = 'win'


class Browser_type(Enum):
    GOOGLE = 'google-chrome'
    CHROMIUM = 'chromium'
    MSEDGE = 'edge'


class ManagerMetaClass(type):
    def __new__(cls, name, bases, attrs):
        if name == 'Manager':
            return type.__new__(cls, name, bases, attrs)

        __pl = sys.platform
        attrs['browser'] = name.lower()
        attrs['os_architecture'] = 64 if sys.maxsize > 2**32 else 32
        attrs['os_name'] = OS_type.LINUX if __pl.startswith(
            'linux') else OS_type.MAC if __pl == 'darwin' else OS_type.WIN
        attrs['os_type'] = f"{attrs['os_name'].value}{attrs['os_architecture']}"
        attrs['chmod'] = cls.chmod

        return type.__new__(cls, name, bases, attrs)

    def chmod(cls, file, per=0o755):
        try:
            os.chmod(file, per)
        except Exception:
            pass


class Manager(metaclass=ManagerMetaClass):
    def __init__(self):
        pass

    def get_ini(self, file):
        self.__ini__ = RawConfigParser()
        self.__ini__.read(file, encoding='utf-8')
        return self.__ini__

    def callback_func(self, blocknum, blocksize, totalsize):
        percent = 100.0 * blocknum * blocksize / totalsize
        if percent > 100:
            percent = 100
        downsize = blocknum * blocksize
        if downsize >= totalsize:
            downsize = totalsize
        s = "%.2f%%" % (percent) + "====>" + "%.2f" % (downsize / 1024 / 1024) + "M/" + "%.2f" % (
            totalsize / 1024 / 1024) + "M \r"
        sys.stdout.write(s)
        sys.stdout.flush()
        if percent == 100:
            print('')

    def shell(self, cmd):
        output, errors = subprocess.Popen(
            cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        self.o = output if output else errors
        return self.o.decode('utf-8')

    def browser_version(self, browser_type):
        cmd_mapping = {
            Browser_type.GOOGLE: {
                OS_type.LINUX: 'google-chrome --version || google-chrome-stable --version',
                OS_type.MAC: r'/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --version',
                OS_type.WIN: r'reg query "HKEY_CURRENT_USER\Software\Google\Chrome\BLBeacon" /v version'
            },
            Browser_type.CHROMIUM: {
                OS_type.LINUX: 'chromium --version || chromium-browser --version',
                OS_type.MAC: r'/Applications/Chromium.app/Contents/MacOS/Chromium --version',
                OS_type.WIN: r'reg query "HKLM\SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall\Google Chrome" /v version'
            },
            Browser_type.MSEDGE: {
                OS_type.LINUX: 'microsoft-edge --version',
                OS_type.MAC: r'/Applications/Microsoft\ Edge.app/Contents/MacOS/Microsoft\ Edge --version',
                OS_type.WIN: r'reg query "HKEY_CURRENT_USER\SOFTWARE\Microsoft\Edge\BLBeacon" /v version',
            }
        }

        cmd = cmd_mapping[browser_type][self.os_name]
        info = self.shell(cmd)
        try:
            return VERSION_RE.findall(info)[0]
        except IndexError:
            print(
                f"Couldn't get version for \"{browser_type.name}\" cause \033[0;31;40m{info}\033[0m")
            sys.exit(-1)

    def download_file(self, url, save_path):
        print(f'will download from \033[0;36;40m{url}\033[0m')
        file = os.path.join(save_path, os.path.basename(url))
        print(f'will saved in \033[0;36;40m{file}\033[0m')
        try:
            urllib.request.urlretrieve(url, file, self.callback_func)
        except ContentTooShortError:
            print(
                f'\033[0;31;40mtimeout!!\033[0m please try again or visit {url}')
            os.remove(file)
            sys.exit(-1)
        print(
            f'Complete!!\r\n\tunpack file list: \033[0;32;40m{self.unpack(file)}\033[0m')

    def unpack(self, file):
        print(f'unpacking {file}')
        if file.endswith('.zip'):
            with zipfile.ZipFile(file, 'r') as zFile:
                try:
                    zFile.extractall(os.path.dirname(file))
                    namelist = zFile.namelist()
                except Exception as e:
                    if e.args[0] not in [26, 13] and e.args[1] not in ['Text file busy', 'Permission denied']:
                        raise e
            return namelist
        elif file.endswith('.tar.gz') or file.endswith('.tgz'):
            try:
                tar = tarfile.open(file, mode='r:gz')
            except tarfile.ReadError:
                tar = tarfile.open(file, mode='r:bz2')
            members = tar.getmembers()
            tar.extractall(os.path.dirname(file))
            tar.close()
            return [x.name for x in members]
