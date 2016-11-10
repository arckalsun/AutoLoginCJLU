#!/usr/bin/env python
# coding:utf-8
# ×Ô¶¯µÇÂ¼CJLU ,½ö¹©ÔÚÖÐ¹ú¼ÆÁ¿´óÑ§Ê¹ÓÃ
# @date:20161019
# @author:arckalsun@gmail.com
# 
#  ÃüÁîÐÐÓÃ·¨£º
#` python login.py username password vpnname vpnusername vpnpassword [anything]`
#  ²ÎÊý½âÊÍ£º
# username ÄÚÍøÕËºÅ
# password ÄÚÍøÃÜÂë
# vpnname VPNÃû×Ö
# vpnusername VPN ÕËºÅ£¬¼´ÍâÍøÕËºÅ
# vpnpassword VPN ÃÜÂë£¬¼´ÍâÍøÃÜÂë
# [anything] ÕâÊÇÒ»¸ö¿ÉÑ¡Ñ¡Ïî£¬Öµ¿ÉÒÔÎªÈÎÒâ×Ö·û´®¡£Èç¹û¼ÓÉÏÕâ¸öÖµ£¬ÔòÖ±½ÓÊ¹ÓÃVPNÁªÍø

# ¿ÉÒÔÐ´¸öÅú´¦ÀíÎÄ¼þ£¬Ð´ÈëÃüÁî£¬´æÎª¿ª»ú×ÔÆô¶¯½Å±¾
# ´Ë³ÌÐòÉÐÎ´ÍêÉÆ£¬²»×ãÖ®´¦Çë´ó¼ÒÔ­ÁÂ£¬»¶Ó­´ó¼ÒÓÅ»¯
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
            #ÄÚÍøÍâÍø¶¼²»¿É·ÃÎÊ
            
            if vpn == "enable":
                print "Ö±½ÓÊ¹ÓÃVPNÁªÍø"
                self.login(self.user, self.passwd, flag = 1)
            else:
                print "ÏÈÁ¬½ÓÐ£Ô°Íø£¬¿´ÄÜ·ñ·ÃÎÊÍâÍø"
                self.login(self.user, self.passwd, flag = 0)
            #ÔÙ¼ì²âÒ»±éÊÇ·ñ³É¹¦ÁªÍø
            self.start(vpn)
            pass
        elif status == 1:
            #²»¿É·ÃÎÊÄÚÍø£¬¿ÉÒÔ·ÃÎÊÍâÍø
            print "ÒÑÁ¬Í¨ÍâÍø£¬²»ÄÜ·ÃÎÊÄÚÍø"
            
        elif status == 2:
            #¿ÉÒÔ·ÃÎÊÄÚÍø£¬²»¿É·ÃÎÊÍâÍø
            self.logout()
            self.login(self.user, self.passwd, flag = 1)
            if vpn == "enable":
                self.connectVPN(vpnname,vpnusername,vpnpassword)
                self.start(vpn)
            else if vpn == "disable":
                print "already connected to school, not connect vpn"
        elif status == 3:
            if vpn == "enable":
                self.logout()
                self.login(self.user, self.passwd, flag = 1)
                self.connectVPN(vpnname,vpnusername,vpnpassword)
                self.start(vpn)
            print "ÒÑÁ¬Í¨ÍâÍø £¬¿ÉÒÔ·ÃÎÊÄÚÍø"
            #ÄÚÍøÍâÍø¶¼¿ÉÒÔ·ÃÎÊ  
    # check network status
    # ·µ»ØÂë£º 
    #           0. ÄÚÍø²»Í¨£¬ÍâÍø²»Í¨
    #           1. ÄÚÍø²»Í¨£¬ÍâÍøÍ¨
    #           2. ÄÚÍøÍ¨£¬  ÍâÍø²»Í¨
    #           3. ÄÚÍøÍ¨£¬  ÍâÍøÍ¨
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
    # »¥ÁªÍøµÇÂ¼ flag = 1, ·ñÔòÎª 0
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
    # Á¬½ÓËæeÐÐ »ò ÉÁÑ¶
    # ÐèÒªÊÂÏÈÅäÖÃºÃVPN
    # ÇëÊÂÏÈÔÚ±¾»ú´´½¨ºÃVPN£¬²ÅÄÜÓÃ´Ëº¯ÊýÆô¶¯
    def connectVPN(self, vpnname, vpnusername, vpnpassword):
	if vpnname==None or vpnusername== None or vpnpassword==None:
		print "no vpn"
		return
        if os.name == 'nt':     # win32
            os.system("rasdial " + vpnname +" " + vpnusername + " " + vpnpassword)
        else:       #unix
            #os.system("pon " + vpnname)
		pass
        
    
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
        try:
            defaultUseVPN = sys.argv[6]
        except:
            defaultUseVPN = ""
            pass
    cjlu = CJLULogin(username, password)
    
    if not defaultUseVPN == "":
        print "ÓÅÏÈÊ¹ÓÃÍâÍø"
        cjlu.start("enable")
    else:
        print "ÓÅÏÈÊ¹ÓÃÐ£Ô°Íø"
        cjlu.start("disable")
    
    
    # check again
    # cjlu.__init__(username, password)

