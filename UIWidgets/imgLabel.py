# python包
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap

# 自建包

# 类
class GaborLabel(QLabel):
    def __init__(self, parent):
        super().__init__(parent)
        self.setScaledContents(True)

    def insertImg(self, path_img):
        pixMap_targetImg = QPixmap(path_img)
        self.setPixmap(QPixmap(""))
        self.setPixmap(pixMap_targetImg)

#测试函数
def test():
    pass

#开启动作
if __name__ == '__main__':
    test()
