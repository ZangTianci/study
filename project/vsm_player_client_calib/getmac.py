#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import platform
import re


class IP2MAC:
    """
    Python3根据IP地址获取MAC地址（不能获取本机IP，可以获取与本机同局域网设备IP的MAC）
    """
    def __init__(self):
        self.patt_mac = re.compile('([a-f0-9]{2}[-:]){5}[a-f0-9]{2}', re.I)

    def getMac(self, ip):
        sysstr = platform.system()

        if sysstr == 'Windows':
            macaddr = self.__forWin(ip)
        elif sysstr == 'Linux':
            macaddr = self.__forLinux(ip)
        else:
            macaddr = None
        if macaddr is None:
            macaddr = '00:00:00:00:00:00'
        macaddr = macaddr.replace(":","")
        macaddr = macaddr.replace("-","")

        return macaddr or '000000000000'

    def __forWin(self, ip):
        os.popen('ping -n 1 -w 500 {} > nul'.format(ip))
        macaddr = os.popen('arp -a {}'.format(ip))
        macaddr = self.patt_mac.search(macaddr.read())

        if macaddr:
            macaddr = macaddr.group()
        else:
            macaddr = None

        return macaddr

    def __forLinux(self, ip):
        os.popen('ping -nq -c 1 -W 500 {} > /dev/null'.format(ip))

        result = os.popen('arp -an {}'.format(ip))

        result = self.patt_mac.search(result.read())

        return result.group() if result else None


if __name__ == '__main__':
    g = IP2MAC()

    print(g.getMac('192.168.1.247'))

