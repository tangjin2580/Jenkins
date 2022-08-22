# -*- coding: utf-8 -*-
import wmi,json
import time

logfile = 'logs_%s.txt' % time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime())

#远程执行bat文件
def call_remote_bat(ipaddress,username,password):
    try:
        #用wmi连接到远程服务器
        conn = wmi.WMI(computer=ipaddress, user=username, password=password)
        filename=r"D:appsautorun.bat"   #此文件在远程服务器上
        cmd_callbat=r"cmd /c call %s"%filename
        conn.Win32_Process.Create(CommandLine=cmd_callbat)  #执行bat文件
        print "执行成功!"
        return True
    except Exception,e:
        log = open(logfile, 'a')
        log.write(('%s, call bat Failed!
') % ipaddress)
        log.close()
        return False
    return False

if __name__=='__main__':
    call_remote_bat(computer="192.168.1.2", user="testuser", password="testpwd")