#!/usr/bin/env python
# coding:utf-8
# 自动登录CJLU ,仅供在中国计量大学使用
# @date:20161019
# @author:arckalsun@gmail.com
# 
#  命令行用法：
# 第一种：
#` python login.py username password vpnname vpnusername vpnpassword`
#  第二种：
#` python login.py username password vpnname vpnusername vpnpassword usevpn`
#  参数解释：
# username 内网账号
# password 内网密码
# vpnname VPN名字
# vpnusername VPN 账号，即外网账号
# vpnpassword VPN 密码，即外网密码
# usevpn 使用vpn，可以是任意非空字符串

# 可以写个批处理文件，写入命令，存为开机自启动脚本
# 此程序尚未完善，不足之处请大家原谅，欢迎大家优化
#
import urllib2,urllib
import sys
import socket
import os
import socket, struct

try:
    import fcntl
except ImportError:
    pass
 

class CJLULogin:
   
    # analyze OS windows/linux
    if (os.name == "nt"):#windows
    # get local ip (windows)
        localip = socket.gethostbyname(socket.gethostname())
    else:#linux or unix
    # get local ip (unix)
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        localip = socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s', 'eth0'[:15]))[20:24])
    print "Local IP : " + localip
    
    def __init__(self, username, password):
        
        self.user = username
        self.passwd = password
        
        
    def start(self,vpn):
    
        status = self.check()
        
            
        
        if status == 0:
            #内网外网都不可访问
            
            if vpn == "enable":
                print "直接使用VPN联网"
                self.login(self.user, self.passwd, flag = 1)
            else:
                print "先连接校园网，看能否访问外网"
                self.login(self.user, self.passwd, flag = 0)
            #再检测一遍是否成功联网
            self.start(vpn)
            pass
        elif status == 1:
            #不可访问内网，可以访问外网
            print "已连通外网，不能访问内网"
            
        elif status == 2:
            #可以访问内网，不可访问外网
            self.logout()
            self.login(self.user, self.passwd, flag = 1)
            self.connectVPN(vpnname,vpnusername,vpnpassword)
            self.start(vpn)
            
        elif status == 3:
            if vpn == "enable":
                self.logout()
                self.login(self.user, self.passwd, flag = 1)
                self.connectVPN(vpnname,vpnusername,vpnpassword)
                self.start()
            print "已连通外网 ，可以访问内网"
            #内网外网都可以访问  
    # check network status
    # 返回码： 
    #           0. 内网不通，外网不通
    #           1. 内网不通，外网通
    #           2. 内网通，  外网不通
    #           3. 内网通，  外网通
    def check(self):
        print "check..."
        InnerUrl = "http://my.cjlu.edu.cn/"
        OuterUrl = "http://www.baidu.com/"
        try:
            InnerResponse = urllib2.urlopen(InnerUrl, timeout = 3)
            InnerFlag = InnerResponse.geturl()
        except (urllib2.URLError, socket.timeout):
            InnerFlag = None
            
        try:
            OuterResponse = urllib2.urlopen(OuterUrl, timeout = 3)
            OuterFlag = OuterResponse.geturl()
        except (urllib2.URLError, socket.timeout):
            OuterFlag = None
        
        
        if (InnerUrl == InnerFlag) & (OuterUrl == OuterFlag):
            print "Connected Internet and School Net!"
            return 3
        elif (InnerUrl == InnerFlag) & (OuterUrl != OuterFlag):
            print "Connected school net but not connected Internet!"
            return 2
        elif (InnerUrl != InnerFlag) & (OuterUrl == OuterFlag):
            print "Connected Internet but cannot visit school net!"
            return 1
        elif (InnerUrl != InnerFlag) & (OuterUrl != OuterFlag):
            print "not connected Internet and school net, please connect "
            return 0
        
        
            
            
    # login
    # 互联网登录 flag = 1, 否则为 0
    def login(self,username,password,flag = 0):
        print "login..."
        url = "https://portal2.cjlu.edu.cn:801/eportal/?c=ACSetting&a=Login&wlanuserip="+self.localip+"&wlanacip=null&wlanacname=&port=&iTermType=1&mac=000000000000&ip="+self.localip+"&redirect=null"
        request = urllib2.Request(url)
        request.add_header('Host','portal2.cjlu.edu.cn:801')
        request.add_header('Connection','keep-alive')
        request.add_header('Cache-Control','max-age=0')
        request.add_header('Origin','https://portal2.cjlu.edu.cn')
        request.add_header('Upgrade-Insecure-Requests','1')
        request.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36')
        request.add_header('Content-Type','application/x-www-form-urlencoded')
        request.add_header('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
        request.add_header('Referer','https://portal2.cjlu.edu.cn/a70.htm?wlanuserip='+self.localip+'&wlanacname=&me60=ethtrunk/2:2775.653')
        request.add_header('Accept-Encoding','gzip, deflate, br')
        request.add_header('Accept-Language','zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4')
        request.add_header('Cookie','wlanacname=; wlanacip=null')
        if flag == 1:
            data = r"DDDDD=__" + username +"&upass="+password+"&R1=0&R2=&R6=0&para=00&0MKKey=123456"
            print "connecting to Internet"
        else:
            data = r"DDDDD=" + username +"&upass="+password+"&R1=0&R2=&R6=0&para=00&0MKKey=123456"
            print "connecting to School LAN"
               
        response = None
        html = None
        error_info = None
        #print request
        response = urllib2.urlopen(request,data)
        info = response.info()
        #print info
        if info['Content-length'] == '10677':
            
            sys.exit('login failed, please check your password')
          
        
    # logout   
    def logout(self):
        print "logout..."
        url = "https://portal2.cjlu.edu.cn:801/eportal/?c=ACSetting&a=Logout&wlanuserip="+self.localip+"&wlanacip=192.168.8.1&wlanacname=me60&port=&iTermType=1"
        #https://portal2.cjlu.edu.cn:801/eportal/?c=ACSetting&a=Logout&wlanuserip=172.28.18.232&wlanacip=192.168.8.1&wlanacname=me60&port=&iTermType=1
        request = urllib2.Request(url)
        request.add_header("Connection","Keep-Alive")
        request.add_header("Origin", "https://portal2.cjlu.edu.cn")
        request.add_header("User-Agent", "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36")
        request.add_header("Content-Type", "application/x-www-form-urlencoded")
        request.add_header("Referer","https://portal2.cjlu.edu.cn/3.htm?wlanuserip=172.28.18.232&wlanacip=192.168.8.1&wlanacname=me60&redirect=&session=")
        request.add_header("Host", "portal2.cjlu.edu.cn:801")
        request.add_header("Accept", "*/*")
        request.add_header("Accept-Encoding", " gzip, deflate, br")
        
        response = None
        html = None
        response = urllib2.urlopen(request, data = "")
        html = response.read()
        
        if len(html) != 10677:
            print "logout error"
    # 连接随e行 或 闪讯
    # 需要事先配置好VPN
    # 请事先在本机创建好VPN，才能用此函数启动
    def connectVPN(self, vpnname, vpnusername, vpnpassword):
	if vpnname==None or vpnusername== None or vpnpassword==None:
		print "no vpn"
		return
        if os.name == 'nt':     # win32
            os.system("rasdial " + vpnname +" " + vpnusername + " " + vpnpassword)
        else:       #unix
            os.system("pon " + vpnname)
        
    
if __name__ == '__main__':

    
    vpnname = None
    vpnusername = None
    vpnpassword = None
    # default not use VPN, False = not use, True = use
    defaultUseVPN = None
    
    if len(sys.argv) < 3:
        #print "Usage: " + sys.argv([0] + " username, password"
        sys.exit("Usage: python " + sys.argv[0] + " username password vpnname vpnusername vpnpassword")
    elif len(sys.argv) < 6:
        print "warning: no vpnname vpnusername vpnpassword"
        username = sys.argv[1]
        password = sys.argv[2]
        
    else:
        username = sys.argv[1]
        password = sys.argv[2]
        vpnname = sys.argv[3]
        vpnusername = sys.argv[4]
        vpnpassword = sys.argv[5]
        defaultUseVPN = sys.argv[6]
    cjlu = CJLULogin(username, password)
    if not defaultUseVPN == "":
        print "优先使用外网"
        cjlu.start("enable")
    else:
        print "优先使用校园网"
        cjlu.start("disable")
    
    
    # check again
    # cjlu.__init__(username, password)

