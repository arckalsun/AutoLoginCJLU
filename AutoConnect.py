import urllib2,urllib
import sys
import socket
import os
import struct
import subprocess
try:
    import fcntl
except ImportError:
    pass
	
#Global vars
username = None
password = None
vpnname = None
vpnusername = None
vpnpassword = None
localip = None




def start():

	if subprocess.call("ping -n 2 baidu.com",shell=True)==0:	#success
		print("already connect Internet!")
		return
	if subprocess.call("ping -n 2 192.168.100.12",shell=True)!=0:
		print("local ip is correct, please check your ip")
		return
	
	
	if subprocess.call("ping -n 2 my.cjlu.edu.cn",shell=True)!=0:	#not login school net
		
		connect()
	else:
		print "reset ip"
		os.system("ipconfig /release")
		os.system("ipconfig /renew")
		connect()

def connect():
	print "login cjlu directly"
	login(0)
	if subprocess.call("ping -n 2 baidu.com",shell=True)==0:#success
		print("already connect Internet!")
		return
	else:
		print "connect failed, please connect cmcc client"
		print "reset ip"
		os.system("ipconfig /release")
		os.system("ipconfig /renew")
		login(1)
		if subprocess.call("ping -n 2 baidu.com",shell=True)==0:
			print "connect success!"
			return
		else:
			print "failed, please run again or check you setting"
			return
# if Connect Internet flag = 1. if not flag = 1
def login(flag = 0):
	print "login..."
	url = "https://portal2.cjlu.edu.cn:801/eportal/?c=ACSetting&a=Login&wlanuserip="+localip+"&wlanacip=null&wlanacname=&port=&iTermType=1&mac=000000000000&ip="+localip+"&redirect=null"
	request = urllib2.Request(url)
	request.add_header('Host','portal2.cjlu.edu.cn:801')
	request.add_header('Connection','keep-alive')
	request.add_header('Cache-Control','max-age=0')
	request.add_header('Origin','https://portal2.cjlu.edu.cn')
	request.add_header('Upgrade-Insecure-Requests','1')
	request.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36')
	request.add_header('Content-Type','application/x-www-form-urlencoded')
	request.add_header('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
	request.add_header('Referer','https://portal2.cjlu.edu.cn/a70.htm?wlanuserip='+localip+'&wlanacname=&me60=ethtrunk/2:2775.653')
	request.add_header('Accept-Encoding','gzip, deflate, br')
	request.add_header('Accept-Language','zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4')
	request.add_header('Cookie','wlanacname=; wlanacip=null')
	if flag == 1:
		data = r"DDDDD=__" + username +"&upass="+password+"&R1=0&R2=&R6=0&para=00&0MKKey=123456"
		print "connecting to Internet"
		urllib2.urlopen(request,data)
		if subprocess.call("ping 192.168.200.1",shell=True)==0:
			print "connecting cmcc client"
			connectVPN()
			print "already connect. if failed, please run again."
			return
		else:
			print "ping cmcc gateway failed"
			return
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
		

def connectVPN():

	if vpnname==None or vpnusername== None or vpnpassword==None:
		print "no vpn"
		return
	if os.name == 'nt':     # win32
		os.system("rasdial " + vpnname +" " + vpnusername + " " + vpnpassword)
	else:       #unix
		#os.system("pon " + vpnname)
		pass		

if __name__ == '__main__':
	# analyze OS windows/linux
	if (os.name == "nt"):#windows
	# get local ip (windows)
		localip = socket.gethostbyname(socket.gethostname())
	else:#linux or unix
	# get local ip (unix)
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		localip = socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s', 'eth0'[:15]))[20:24])
	print "Local IP : " + localip
	
	if len(sys.argv) < 3:
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
	#start
	start()