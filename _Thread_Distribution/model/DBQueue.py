#coding:utf-8

from queue import Queue
FilePath = '..\db'
'''
import sqlite3  #Sql版本可以实现不过比较复杂不适合轻量级代码  换成ini文件更容易操作

class MySql():
    def __init__(self):
        
        self.db = sqlite3.connect('userinfo.db')
        
    def __del__(self):
        
        self.db.close()
    
    def __add(self,useroinfo):
        
        self.cr = self.db.cursor()
        
        Sql = 'insert into userinfo(hostname,port,name,username,passwd) values(\'%s\',%s,\'%s\',\'%s\',\'%s\')' % userinfo
        if self.cr.execute(Sql):
            self.db.commit() 
    
    def __load(self): 
    '''

class DBQueue(Queue):
    '''
    def __init__(self):
        
        super(_db,self).__init__()
    '''
    '''
    def __add(self,hostname,port,name,username,passwd):#用json添加到本地数据库中
        
        self.__db.append(hostname)
        self.__db.append(port)
        self.__db.append(name)
        self.__db.append(username)
        self.__db.append(passwd)
    '''
    def __init__(self):
        
        super(DBQueue,self).__init__()
        
        num,temp_db = self.LoadDBQueue()
        for i in range(0,num-1):
            self.put(temp_db[i])
            
        print("数据加载Queue完成,共完成%d条" % (self.qsize(),))
        
        
    def LoadDBQueue(self):
        
        fp = open(FilePath,'r')
        _userinfo = []
        num = 1
        for line in fp:
            if num == 1 and line == '':
                print("配置文件中没有数据可以加载")
            else:
                _userinfo.append(line.split(':'))
                num+=1
        print("数据加载到内存完成,加载%d条" % (num-1,))
        return((num,_userinfo))
            

        
        
        
        
        
    