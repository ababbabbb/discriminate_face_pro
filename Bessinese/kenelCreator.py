# python包
from abc import abstractmethod, ABCMeta
import cv2
import numpy as np

# 自建包
from CodeTools.loggingTool import GaborLogger

#类
class KenelBasic(metaclass=ABCMeta):
    def __init__(self):
        pass

    @abstractmethod
    def filterBuild(self):
        pass

    @abstractmethod
    def getGabor(self, img):
        pass


class CustomizeKenel(KenelBasic):
    def __init__(self):
        super().__init__()
        ...

    def filterBuild(self):
        pass

    def getGabor(self, img):
        pass

class GaborKenel(KenelBasic):
    def __init__(self):
        super().__init__()
        self.logger = GaborLogger('GaborKenel')
        self.filters = []

    def filterBuild(self):
        self.logger.getFuncName('filterBuild')
        self.logger.normalInfo('设置尺度及滤波器容器')
        ksize = [13, 15, 17, 19, 21, 23]  # gabor尺度，6个
        lamda = np.pi / 2.0  # 波长
        self.logger.normalInfo('创建滤波器')
        for theta in np.arange(0, np.pi*0.75, np.pi / 4):  # gabor方向，0°，45°，90°，135°，共四个
            for K in range(6):
                kern = cv2.getGaborKernel((ksize[K], ksize[K]), 1.0, theta, lamda, 0.5, 0, ktype=cv2.CV_32F)
                kern /= 1.5 * kern.sum()
                self.filters.append(kern)

        self.logger.varInfo(self.filters)

    def getGabor(self, img):
        self.logger.getFuncName('getGabor')
        self.logger.normalInfo('使用滤波器处理图像')
        accum = np.zeros_like(img)  # 创建全零矩阵
        for kern in self.filters:
            fimg = cv2.filter2D(img, cv2.CV_32FC1, kern)  # 使用滤波核对图片滤波
            accum = np.maximum(accum, fimg, accum)  # 逐步叠加滤波效果

        self.logger.varInfo(accum)
        return accum

    def meanPooling(self, img, G=3):
        self.logger.getFuncName('meanPooling')
        self.logger.normalInfo('设置长宽高等值')
        out = img.copy()  # 此时图片为RGB格式——C, H, W
        C, H, W = img.shape
        Nh = int(H / G)
        Nw = int(W / G)

        self.logger.normalInfo('进入像素块平均化嵌套循环')
        for i in range(Nh):
            for j in range(Nw):
                for c in range(C):
                    out[c, G * i:G * (i + 1), G * j:G * (j + 1)] = np.mean(
                        out[c, G * i: G * (i + 1), G * j: G * (j + 1)]).astype(
                        np.int)

        out = out/255
        self.logger.varInfo('池化后结果-> '+str(out))
        return out


#测试函数
def test():
    pass

#开启动作
if __name__ == '__main__':
    test()
