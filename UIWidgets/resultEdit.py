# python包
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtGui import QFont

# 自建包
from CodeTools.loggingTool import GaborLogger

# 类
class GaborEdit(QLineEdit):
    def __init__(self, parent):
        super().__init__(parent)
        self.setReadOnly(True)
        self.setFont(QFont("Timers", 50, QFont.Bold))

    def getResult(self, str_result):
        self.setText(str_result)

# 测试函数
def test():
    pass

#开启动作
if __name__ == '__main__':
    test()
