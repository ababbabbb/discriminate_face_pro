# python包
import qdarkstyle
import sys
import os
import cv2
import numpy as np
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QImage, QPixmap, QFont

# 自建包
import CodeTools.loggingTool as logTool
from CodeTools.loggingTool import GaborLogger
from UIWidgets.resultEdit import GaborEdit
from UIWidgets.imgLabel import GaborLabel
from UIWidgets.trainStateWindow import GaborChildWindow
from Bessinese.discriminate import GaborDiscriminatr

# 类
class GaborLogsVar():
    def __init__(self):
        # 日志共用变量初始化
        self.path_exe = logTool.GaborLogFolder.path_exe
        self.global_tlf = logTool.GaborLogFolder.topFolder_log
        self.global_lf = logTool.GaborLogFolder.folder_log
        self.global_fb = logTool.GaborLogFile.flie_bessineseLog
        self.global_fv = logTool.GaborLogFile.file_varLog


class GaborFaceUI(QMainWindow):
    def __init__(self):
        super(GaborFaceUI, self).__init__(parent=None)
        self.setWindowTitle('基于gabor的人脸识别')
        self.resize(900, 600)
        self.logger = GaborLogger('GaborFaceUI')
        self.logger.normalInfo('主窗体初始化')
        self.obj_discriminate = GaborDiscriminatr()

        self.initVessel()
        self.initWidgets()
        self.initTopologica()

    def initVessel(self):
        # 初始化容器

        pass

    def initWidgets(self):
        self.logger.getFuncName('initWidgets')
        # 初始化控件
        self.logger.normalInfo('初始化控件')
        # 按钮
        self.button_train = QPushButton("训练AI", self)
        self.button_train.setFont(QFont("Timers", 30, QFont.Bold))
        self.button_train.clicked.connect(self.trainModel)

        self.button_insert = QPushButton("导入", self)
        self.button_insert.setFont(QFont("Timers", 30, QFont.Bold))
        self.button_insert.clicked.connect(self.insertImg)

        self.button_discriminate = QPushButton("人脸识别", self)
        self.button_discriminate.setFont(QFont("Timers", 30, QFont.Bold))
        self.button_discriminate.clicked.connect(self.discriminate)

        # 文本框
        self.lineEdit_result = GaborEdit(self)

        # 图片展示框
        self.label_targetImg = GaborLabel(self)
        self.label_targetImg.resize(600, 600)

    def initTopologica(self):
        self.logger.getFuncName('initTopologica')
        # 布局界面控件
        hspliter = QSplitter(Qt.Horizontal)
        hspliter.resize(900, 600)
        vspliter = QSplitter(Qt.Vertical)
        vspliter.resize(300, 600)

        # 右侧垂直控件排布
        vspliter.addWidget(self.lineEdit_result)
        vspliter.addWidget(self.button_train)
        vspliter.addWidget(self.button_insert)
        vspliter.addWidget(self.button_discriminate)

        # 整体从左到右水平排布
        hspliter.addWidget(self.label_targetImg)
        hspliter.addWidget(vspliter)

        self.logger.normalInfo('布局完成，并开始展示')
        self.setCentralWidget(hspliter)

    def trainModel(self):
        self.logger.getFuncName('trainModel')
        self.logger.normalInfo('弹出阻塞子窗口')
        self.childWindow = GaborChildWindow(self)
        self.logger.normalInfo('进入模型训练与构建')
        try:
            self.obj_discriminate.buildModel(self.childWindow)
        except:
            self.logger.tranceInfo()
            self.childWindow.close()
            dlg = QMessageBox(self)
            dlg.setIcon(QMessageBox.Critical)
            dlg.setText('训练失败')
            dlg.show()
        else:
            self.childWindow.close()

    def trainStop(self):
        self.logger.getFuncName('trainStop')
        self.logger.getFuncName('结束训练')
        self.obj_discriminate.stopTrain()
        dlg = QMessageBox(self)
        dlg.setIcon(QMessageBox.Critical)
        dlg.setText('训练已关闭')
        dlg.show()

    def discriminate(self):
        self.logger.getFuncName('discriminate')
        if self.path_targetImg is not None:
            result, img_gray, img_gabored, img_meanPool = self.obj_discriminate.discriminate(self.path_targetImg)
            self.logger.varInfo(str(result))
        else:
            self.logger.abnormalInfo('导入图片路径为空')
            dlg = QMessageBox(self)
            dlg.setIcon(QMessageBox.Critical)
            dlg.setText('当前无导入图片')
            dlg.show()
            return 0

        if result != 0:
            self.logger.normalInfo('当前为人脸')
            str_insertToEdit = '当前为人脸,身份为——'+str(result)
            path_exe = os.getcwd()
            path_fier = path_exe+'\\faceRes\\faceFier\\haarcascade_frontalface_alt2.xml'
            self.logger.normalInfo('圈出人脸范围')
            classfier = cv2.CascadeClassifier(path_fier)
            color = (0, 255, 0)
            faceRects = classfier.detectMultiScale(self.img_target, scaleFactor=1.2, minNeighbors=2, minSize=(32, 32))
            for faceRect in faceRects:
                x, y, w, h = faceRect
                cv2.rectangle(self.img_target, (x - 10, y - 10), (x + w + 10, y + h + 10), color, 2)

            height, width, channel = self.img_target.shape
            bytesPerLine = 3 * width
            self.logger.normalInfo('转换为QImg形式并展示')
            self.qImg = QImage(self.img_target, width, height, bytesPerLine,
                               QImage.Format_RGB888).rgbSwapped()
            self.label_targetImg.setPixmap(QPixmap.fromImage(self.qImg))
        else:
            self.logger.normalInfo('当前非人脸')
            str_insertToEdit = '当前非人脸'

        self.lineEdit_result.getResult(str_insertToEdit)

        img_gray = img_gray.astype('uint8')
        img_gabored = img_gabored.astype('uint8')
        img_meanPool = img_meanPool.astype('uint8')
        imgStack = np.hstack((img_gray, img_gabored, img_meanPool))
        cv2.imshow('processShow', imgStack)
        cv2.waitKey(0)

    def insertImg(self):
        self.logger.normalInfo('导入图片')
        try:
            path, _ = QFileDialog.getOpenFileName(self, '打开文件', '', '文件(*.pgm *.jpg)')
            if path is not None and path != '':
                self.path_targetImg = path
            else:
                return 0
        except Exception as e:
            self.logger.warringInfo(str(e))

        self.logger.normalInfo('opencv打开图片')
        self.img_target = cv2.imread(self.path_targetImg)
        height, width, channel = self.img_target.shape
        bytesPerLine = 3 * width
        self.logger.normalInfo('转换为QImg形式并展示')
        self.qImg = QImage(self.img_target, width, height, bytesPerLine,
                           QImage.Format_RGB888).rgbSwapped()
        self.label_targetImg.setPixmap(QPixmap.fromImage(self.qImg))

        self.logger.varInfo(str(self.img_target))

# 测试函数
def test():
    pass

#开启动作
if __name__ == '__main__':
    loggerVar = GaborLogsVar()
    logger = GaborLogger('main')
    try:
        app = QApplication(sys.argv)
        UI = GaborFaceUI()
        UI.showMaximized()
        app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))
        UI.show()
        if app.exec_():
            UI.logic.__db_currentCartons.close()
            UI.logic.__db_highDensityCartons.close()
            sys.exit()
    except:
        logger.tranceInfo()
