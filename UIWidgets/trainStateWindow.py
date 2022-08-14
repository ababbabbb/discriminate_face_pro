# python包
from PyQt5.QtWidgets import QDialog, QLabel, QHBoxLayout, QVBoxLayout, QProgressBar, QPushButton
from PyQt5.QtCore import Qt

# 自建包
from CodeTools.loggingTool import GaborLogger

#类
class GaborChildWindow(QDialog):

    def __init__(self, parent=None):
        super(GaborChildWindow, self).__init__(parent)
        self.logger = GaborLogger('GaborChildWindow')
        self.logger.normalInfo('设置窗体样式')
        self.mainWindow = parent
        self.setWindowTitle('')
        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        # self.setAttribute(Qt.WA_TranslucentBackground)
        self.resize(700, 260)

        self.logger.normalInfo('构造掩盖窗体控件')

        self.label = QLabel('训练进行中')

        self.featProgressBar = QProgressBar(self)
        self.featProgressBar.setMinimum(0)
        self.featProgressBar.setMaximum(100)
        self.featProgressBar.setValue(0)

        self.stopButton = QPushButton(self)
        self.stopButton.setText('STOP')
        self.stopButton.clicked.connect(self.endWindow)

        labelLayout = QHBoxLayout()
        labelLayout.addWidget(self.label)

        processBarLayout = QHBoxLayout()
        processBarLayout.addWidget(self.featProgressBar)

        stopButtonLayout = QHBoxLayout()
        stopButtonLayout.addWidget(self.stopButton)

        layout = QVBoxLayout()
        layout.addLayout(labelLayout)
        layout.addLayout(processBarLayout)
        layout.addLayout(stopButtonLayout)
        self.setLayout(layout)

        self.logger.normalInfo('展示掩盖窗体')
        self.show()

    def setValue(self, value):
        self.logger.getFuncName('setValue')
        self.logger.normalInfo('设进度条值为'+str(value))
        self.featProgressBar.setValue(value)

    def endWindow(self):
        self.logger.getFuncName('endWindow')
        self.logger.normalInfo('中止训练')
        self.close()
        self.mainWindow.trainStop()


# 测试函数
def test():
    pass

# 开启动作
if __name__ == '__main__':
    test()
