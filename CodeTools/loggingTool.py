# python包
import os
import time
import tracebackturbo as traceback

# 自建包

# 类
class GaborLogFolder:
    path_exe = os.getcwd()
    topFolder_log = path_exe + '\\Gaborlogs'
    folder_log = topFolder_log + time.strftime('\\%Y-%m-%d,%H-%M-%S')
    if os.path.exists(topFolder_log):
        pass
    else:
        os.mkdir(topFolder_log)

    if os.path.exists(folder_log):
        pass
    else:
        os.mkdir(folder_log)

class GaborLogFile:
    flie_bessineseLog = GaborLogFolder.folder_log + '\\bessibese.txt'
    file_varLog = GaborLogFolder.folder_log + '\\varLog.txt'

class GaborLogger(object):
    def __init__(self,  name_class):
        self.path_bessineseLog = GaborLogFile.flie_bessineseLog
        self.path_varLog = GaborLogFile.file_varLog
        self.name_class = name_class
        self.initInfo()

    def initInfo(self):
        fb = open(self.path_bessineseLog, 'a+')
        fv = open(self.path_varLog, 'a+')
        print(time.strftime('%H:%M:%S -> ') + 'class ->' + self.name_class + 'is running', file=fb)
        fb.close()
        fv.close()

    def getFuncName(self, str_info):
        fb = open(self.path_bessineseLog, 'a+')
        fv = open(self.path_varLog, 'a+')
        print(time.strftime('%H:%M:%S ->') + self.name_class +
              '|func ->'+ str_info + ' is running', file=fb)
        fb.close()
        fv.close()

    def normalInfo(self, str_info):
        fb = open(self.path_bessineseLog, 'a+')
        fv = open(self.path_varLog, 'a+')
        print(time.strftime('%H:%M:%S ->') + self.name_class +
              '|正常 —>\n' + str_info, file=fb)
        fb.close()
        fv.close()

    def abnormalInfo(self, str_info):
        fb = open(self.path_bessineseLog, 'a+')
        fv = open(self.path_varLog, 'a+')
        print(time.strftime('%H:%M:%S ->') + self.name_class +
              '|异常 —>\n' + str_info, file=fb)
        fb.close()
        fv.close()

    def warringInfo(self, str_info):
        fb = open(self.path_bessineseLog, 'a+')
        fv = open(self.path_varLog, 'a+')
        print(time.strftime('%H:%M:%S ->') + self.name_class +
              '|错误 —>\n' + str_info, file=fb)
        fb.close()
        fv.close()

    def tranceInfo(self):
        fb = open(self.path_bessineseLog, 'a+')
        fv = open(self.path_varLog, 'a+')
        print(time.strftime('%H:%M:%S ->') + self.name_class +
              '|回溯 —>\n', file=fb)
        fb.close()
        fb = open(self.path_bessineseLog, 'a+')
        traceback.print_exc(file=fb)
        fb.close()
        fv.close()

    def varInfo(self, str_info):
        fb = open(self.path_bessineseLog, 'a+')
        fv = open(self.path_varLog, 'a+')
        print(time.strftime('%H:%M:%S ->') + self.name_class +
              '|变量变更 —>\n', file=fv)
        print(str_info, file=fv)
        fb.close()
        fv.close()


# 测试函数
def test():
    pass


# 开启动作
if __name__ == '__main__':
    test()
