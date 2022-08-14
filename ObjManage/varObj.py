# python包

# 自建包
from CodeTools.loggingTool import GaborLogger

# 类
class GaborGlobalVessel():

    def __init__(self):
        self.globalVessel = []

class GaborVessel():
    def __init__(self, projectName):
        self.logger = GaborLogger('GaborVessel')
        self.logger.normalInfo('开始初始化')
        self.vessel_project = [projectName]

        self.vessel_kenelImg = []
        kenelImg = None
        property_k = {
            'path': None
        }
        self.vessel_kenelImg.append(kenelImg)
        self.vessel_kenelImg.append(property_k)

        self.vessel_targetImg = []
        targetImg = None
        property_t = {
            'path': None
        }
        self.vessel_kenelImg.append(targetImg)
        self.vessel_kenelImg.append(property_t)

        self.vessel_project.append(self.vessel_kenelImg)
        self.vessel_project.append(self.vessel_targetImg)

        self.logger.normalInfo('初始化完毕')
        self.logger.varInfo(self.vessel_project)

    def kenelImgInsert(self, kenelImg):
        self.logger.normalInfo('更换kenel内容')
        self.vessel_kenelImg[0] = kenelImg
        self.logger.normalInfo('更换完毕')

    def targetImgInsert(self, targetImg, path_t):
        self.logger.normalInfo('更换目标图片内容')
        self.vessel_targetImg[0] = targetImg
        self.vessel_targetImg[1]['path'] = path_t
        self.logger.normalInfo('更换目标图片内容完毕')
        self.logger.varInfo(self.vessel_project)


#测试函数
def test():
    pass

#开启动作
if __name__ == '__main__':
    test()
