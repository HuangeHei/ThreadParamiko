#coding:utf-8

from model.Thread_Paramiko import Thread_Paramiko
from model.DBQueue import DBQueue


                
if __name__ =='__main__':
    
    UserDBQueue = DBQueue()
    
    '''字典在此处应用有个缺陷就是ServerName无法重复(Key=Servername)'''
    
    Cmd = {} #控制消息队列的字典
    
    for i in range(0,UserDBQueue.qsize()):
        
        if not UserDBQueue.empty():
            
            UserInfo = UserDBQueue.get()
            Th = Thread_Paramiko(UserInfo)
            Cmd[UserInfo[2]] = Th.getqueue()
            Th.start()


    flag = True
    while flag:
        
        CmdBuffs = input("请输入命令:")
        
        if CmdBuffs == 'Quit' or CmdBuffs == 'quit' :
            for (k,v) in Cmd.items():
                v.put('Quit')
            flag = False
        else:
            for (k,v) in Cmd.items():
                v.put(CmdBuffs)
           
    print('欢迎使用,下次再见')         


