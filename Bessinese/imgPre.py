# python包
import cv2

# 自建包
from CodeTools.loggingTool import GaborLogger

# 类
class GaborImgPre():
    def __init__(self):
        self.logger = GaborLogger('GaborImgPre')

    def preFunc(self, path_targetImg):
        self.logger.getFuncName('preFunc')
        self.logger.normalInfo('导入图片')
        image = cv2.imread(path_targetImg)  # 此时图片格式为BGR——H,W,C

        self.logger.normalInfo('灰度化')
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        self.logger.varInfo(str(gray))

        H, W = gray.shape
        if H != 218 or W != 178:
            gray = cv2.resize(gray, (178, 218), interpolation=cv2.INTER_CUBIC)

        gray = gray.astype('float32')

        gray = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
        gray = cv2.cvtColor(gray, cv2.COLOR_BGR2RGB)

        return gray

# 测试函数
def test():
    obj_thisPy = GaborImgPre()
    img_gray = obj_thisPy.preFunc("C:\\Users\\17826\\Desktop\\000065.jpg")
    img_gray = img_gray.astype('uint8')
    cv2.imshow('阿布', img_gray)
    img_old = cv2.imread("C:\\Users\\17826\\Desktop\\000065.jpg")
    cv2.imshow('aa', img_old)
    cv2.waitKey(0)

# 开启动作
if __name__ == '__main__':
    test()
