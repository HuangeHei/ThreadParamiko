#coding:utf-8

from threading import Thread
from queue import Queue
import paramiko
import time


class Thread_Paramiko(Thread): 
    
    '''
    paramiko 多线程实现命令分发
    '''

    def __init__(self,UserInfo):
        
        super(Thread_Paramiko,self).__init__()#初始化父类
        
        '''__CmdQueue是Cmd消息队列,设为私有更安全
        '''
        
        self.__CmdQueue = Queue()
        self.__Host = UserInfo
        
        '''把ServerName当作进程名字,这样为以后线程管理做打算
        '''
        self._name = self.__Host[2] 
        
        '''self.DBQueue = DBQueue
        DBQueue不由各线程控制，用户信息由主线程控制,用户信息由函数参数传进__Host Ps:有想法把列表改为字典，这样代码更易阅读
        if not self.DBQueue.empty():   
            self.__Host = self.DBQueue.get()
        ''' 
        '''self.__Host 元素对照表
        self.__Host[0]  ==  hostname
        self.__Host[1]  ==  port
        self.__Host[2]  ==  servername
        self.__Host[3]  ==  username
        self.__host[4]  ==  passwd
        '''
            
    def __del__(self):
        
        print("服务器:%s执行完成线程结束" % (self.__Host[2],))

        
    def connect(self):#进行ssh连接用密码
        
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        try:
            self.__Host[4] = self.__Host[4].strip()
            self.ssh.connect(self.__Host[0],port=int(self.__Host[1]),username=self.__Host[3],password=self.__Host[4])
        
        except paramiko.ssh_exception.AuthenticationException as err:#Paramiko自定义异常，代表了认证失败
            
            if err.__str__() == "Authentication failed.":#自定义异常都会写一个str方法来装错误信息
                print("服务器:%s\t认证错误请检查用户名或密码" % (self.__Host[2],))
                return -1#返回错误
            
        except TimeoutError as err:

            print("服务器:%s  Error:%s" % (self.__Host[2],err))
            return -1#返回错误
        
        else:
            print("服务器:%s\t加载成功" % (self.__Host[2],))
            
            
        
    def exec_command(self,cmd):#命令用完结束
        
        '''此处代码不够稳健，没做异常
        '''
    
        stdin,stdout,stderr = self.ssh.exec_command(cmd)
        ret = stdout.read().decode('utf-8')
        
        if ret:
            print('服务器:%s\t命令执行成功' % (self.__Host[2],))
            self.log(ret,cmd)#结果写入日志
        else:
            print('服务器:%s\t命令执行未成功' % (self.__Host[2],))
            return -1
        
        
    
    def log(self,ret,cmd):#日志写入
        
        fp = open(('%s_cmd.log' % (self.__Host[2],)),'a')#以追加打开文件，如果没有则创建
        
        nowtime = time.strftime('%Y-%m-%d %X',time.localtime(time.time()))#获取时间
        
        #时间，命令，是否成功，内容
        if fp.write(('%s\t \'%s\' \tOK\tret->\n-----------------------------------------------\
            \n%s-----------------------------------------------\n' % (nowtime,cmd,ret,))):
            print('服务器:%s\t执行结果已成功写入日志' % (self.__Host[2],))
            #检测结果是否成功写入，否的话就没写入
        else:
            print('服务器:%s\t执行结果未成功写入日志' % (self.__Host[2],))
            fp.close()
            
    
    def getqueue(self): 
        '''
                    返回消息队列给主线程
        '''
        return(self.__CmdQueue)
        
        
    def run(self):
        
        
        if self.connect():
            #print("服务器:%s发生不可逆的错误\t线程结束" % (self.__Host[2],))
            return -1
        
        else:
            flag = True
            
            while flag:
                
                if  not self.__CmdQueue.empty() :
                    
                    CmdTemp = self.__CmdQueue.get()
                    
                    if CmdTemp == 'Quit':
                        flag = False
                    else:
                        self.exec_command(CmdTemp)
                    
                else:
                    time.sleep(0.1)
                
                