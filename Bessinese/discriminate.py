# python包
import os
import numpy as np
import tensorflow as tf

# 自建包
import random
from Bessinese.imgPre import GaborImgPre
from Bessinese.kenelCreator import GaborKenel
from Bessinese.bpNet import GaborBPNetModel
from CodeTools.loggingTool import GaborLogger

# 类
class GaborDiscriminatr():
    def __init__(self):
        self.logger = GaborLogger('GaborDiscriminatr')
        self.logger.normalInfo('初始化目标图片——灰度&归一化')
        self.obj_imgPre = GaborImgPre()
        self.obj_GaborKenel = GaborKenel()
        self.obj_GaborKenel.filterBuild()
        self.obj_GaborBPModel = GaborBPNetModel()
        self.imgs_train = []
        self.imgs_valid = []
        self.labels_train = []
        self.labels_valid = []

    def dataSet(self, processBar):
        self.logger.getFuncName('dataSet')
        self.logger.normalInfo('设置样本及标签')
        path_exe = os.getcwd()
        path_baseData = path_exe + '\\faceRes'
        if os.path.exists(path_baseData):
            pass
        else:
            self.logger.abnormalInfo('程序下无对应路径')
            return None, None, None, None

        path_humanImgs = path_baseData + '\\imgs_human'
        path_unhumanImgs = path_baseData + '\\imgs_unhuman'

        processBar.setValue(10)

        self.logger.normalInfo('进入100训练样本制作循环')
        value_add_train = 10
        for t in range(0, 2000):
            value_add_train += 0.01
            index_human = str(random.randint(1, 202599))
            name_humanImg = str(index_human.zfill(6))
            self.logger.varInfo('此时训练样本图片名称为->human-> '+str(name_humanImg))
            self.logger.varInfo('同时其路径为-> '+str(path_humanImgs+'\\'+name_humanImg+'.jpg'))
            img_human = self.obj_imgPre.preFunc(path_humanImgs+'\\'+name_humanImg+'.jpg')
            meanImg_human = self.obj_GaborKenel.meanPooling(self.obj_GaborKenel.getGabor(img_human))
            self.imgs_train.append(meanImg_human)  # 添加处理后的图片到列表
            self.labels_train.append(1)

            processBar.setValue(value_add_train)
            value_add_train += 0.01

            result_unhuman_train = False
            while result_unhuman_train != True:
                index_unhuman = random.randint(1, 7300)
                imgs_unhuman = os.listdir(path_unhumanImgs)
                self.logger.varInfo('此时训练样本图片名称为->unhuman-> ' + str(imgs_unhuman[index_unhuman]))
                self.logger.varInfo('同时其路径为-> ' + str(path_unhumanImgs + '\\' + str(imgs_unhuman[index_unhuman])))
                try:
                    img_unhuman = self.obj_imgPre.preFunc(path_unhumanImgs + '\\' + str(imgs_unhuman[index_unhuman]))
                    meanImg_unhuman = self.obj_GaborKenel.meanPooling(self.obj_GaborKenel.getGabor(img_unhuman))
                    self.imgs_train.append(meanImg_unhuman)
                    self.labels_train.append(0)
                except:
                    self.logger.normalInfo('这个路径有问题')
                    self.logger.tranceInfo()
                    result_unhuman_train = False
                    continue
                else:
                    result_unhuman_train = True

            processBar.setValue(value_add_train)

        self.logger.normalInfo('进入500测试样本循环')
        value_add_test = 30
        for v in range(0, 500):
            value_add_test += 0.04
            index_human = str(random.randint(1, 202599))
            name_humanImg = index_human.zfill(6)
            img_human = self.obj_imgPre.preFunc(path_humanImgs + '\\' + name_humanImg + '.jpg')
            meanImg_human = self.obj_GaborKenel.meanPooling(self.obj_GaborKenel.getGabor(img_human))
            self.imgs_valid.append(meanImg_human)  # 添加处理后的图片到列表
            self.labels_valid.append(1)

            processBar.setValue(value_add_test)
            result_unhuman_valid = False
            while result_unhuman_valid != True:
                index_unhuman = random.randint(1, 7390)
                imgs_unhuman = os.listdir(path_unhumanImgs)
                try:
                    img_unhuman = self.obj_imgPre.preFunc(path_unhumanImgs + '\\' + str(imgs_unhuman[index_unhuman]))
                    meanImg_unhuman = self.obj_GaborKenel.meanPooling(self.obj_GaborKenel.getGabor(img_unhuman))
                    self.imgs_valid.append(meanImg_unhuman)
                    self.labels_valid.append(0)
                except:
                    self.logger.tranceInfo()
                    result_unhuman_valid = False
                    continue
                else:
                    result_unhuman_valid = True

        self.logger.normalInfo('图片数组化')
        self.imgs_train_np = np.array(self.imgs_train)
        self.labels_train_np = tf.one_hot(np.array(self.labels_train), 2)
        self.imgs_valid_np = np.array(self.imgs_valid)
        self.labels_valid_np = tf.one_hot(np.array(self.labels_valid), 2)

        processBar.setValue(55)

        self.logger.varInfo('训练数据及标签')
        self.logger.varInfo(str(self.imgs_train_np)+'\n 形状为\n'+str(self.imgs_train_np.shape))
        self.logger.varInfo(str(self.labels_train_np)+'\n 形状为\n'+str(self.labels_train_np.shape))
        self.logger.varInfo('测试数据及标签')
        self.logger.varInfo(str(self.imgs_valid_np)+'\n 形状为\n'+str(self.imgs_valid_np.shape))
        self.logger.varInfo(str(self.labels_valid_np)+'\n 形状为\n'+str(self.labels_valid_np.shape))

        self.logger.normalInfo('样本及标签数据制作结束')
        return self.imgs_train_np, self.labels_train_np, self.imgs_valid_np, self.labels_valid_np

    def dataSet_Id(self, processBar):
        self.logger.getFuncName('dataSet')
        self.logger.normalInfo('设置样本及标签')
        path_exe = os.getcwd()
        path_baseData = path_exe + '\\faceRes'
        if os.path.exists(path_baseData):
            pass
        else:
            self.logger.abnormalInfo('程序下无对应路径')
            return None, None, None, None

        path_humanImgs = path_baseData + '\\imgs_person\\all'
        path_unhumanImgs = path_baseData + '\\imgs_unhuman'

        processBar.setValue(10)

        self.logger.normalInfo('进入100训练样本制作循环')
        value_add_train = 10
        for t in range(0, 1200):
            value_add_train += 0.01
            index_human = str(random.randint(1, 1500))
            name_humanImg = 'BioID_' + str(index_human.zfill(4)) + '.pgm'
            self.logger.varInfo('此时训练样本图片名称为->human-> ' + str(name_humanImg))
            self.logger.varInfo('同时其路径为-> ' + str(path_humanImgs + '\\' + name_humanImg))
            img_human = self.obj_imgPre.preFunc(path_humanImgs + '\\' + name_humanImg)
            meanImg_human = self.obj_GaborKenel.meanPooling(self.obj_GaborKenel.getGabor(img_human))
            self.imgs_train.append(meanImg_human)  # 添加处理后的图片到列表
            for n in range(1, 24):
                path_hunmanImgLabel = path_baseData + '\\imgs_person\\' + str(n)
                currentFiles = os.listdir(path_hunmanImgLabel)
                if name_humanImg in currentFiles:
                    num_label = n
                    break
                else:
                    continue
            self.labels_train.append(num_label)

            processBar.setValue(value_add_train)
            value_add_train += 0.01

            result_unhuman_train = False
            while result_unhuman_train != True:
                index_unhuman = random.randint(1, 7300)
                imgs_unhuman = os.listdir(path_unhumanImgs)
                self.logger.varInfo('此时训练样本图片名称为->unhuman-> ' + str(imgs_unhuman[index_unhuman]))
                self.logger.varInfo('同时其路径为-> ' + str(path_unhumanImgs + '\\' + str(imgs_unhuman[index_unhuman])))
                try:
                    img_unhuman = self.obj_imgPre.preFunc(path_unhumanImgs + '\\' + str(imgs_unhuman[index_unhuman]))
                    meanImg_unhuman = self.obj_GaborKenel.meanPooling(self.obj_GaborKenel.getGabor(img_unhuman))
                    self.imgs_train.append(meanImg_unhuman)
                    self.labels_train.append(0)
                except:
                    self.logger.normalInfo('这个路径有问题')
                    self.logger.tranceInfo()
                    result_unhuman_train = False
                    continue
                else:
                    result_unhuman_train = True

            processBar.setValue(value_add_train)

        self.logger.normalInfo('进入500测试样本循环')
        value_add_test = 30
        for v in range(0, 500):
            value_add_test += 0.04
            index_human = str(random.randint(1, 1500))
            name_humanImg = 'BioID_' + str(index_human.zfill(4)) + '.pgm'
            self.logger.varInfo('此时训练样本图片名称为->human-> ' + str(name_humanImg))
            self.logger.varInfo('同时其路径为-> ' + str(path_humanImgs + '\\' + name_humanImg))
            img_human = self.obj_imgPre.preFunc(path_humanImgs + '\\' + name_humanImg)
            meanImg_human = self.obj_GaborKenel.meanPooling(self.obj_GaborKenel.getGabor(img_human))
            self.imgs_valid.append(meanImg_human)  # 添加处理后的图片到列表
            for n in range(1, 24):
                path_hunmanImgLabel = path_baseData + '\\imgs_person\\' + str(n)
                currentFiles = os.listdir(path_hunmanImgLabel)
                if name_humanImg in currentFiles:
                    num_label = n
                    break
                else:
                    continue
            self.labels_valid.append(num_label)

            processBar.setValue(value_add_test)
            result_unhuman_valid = False
            while result_unhuman_valid != True:
                index_unhuman = random.randint(1, 7390)
                imgs_unhuman = os.listdir(path_unhumanImgs)
                try:
                    img_unhuman = self.obj_imgPre.preFunc(path_unhumanImgs + '\\' + str(imgs_unhuman[index_unhuman]))
                    meanImg_unhuman = self.obj_GaborKenel.meanPooling(self.obj_GaborKenel.getGabor(img_unhuman))
                    self.imgs_valid.append(meanImg_unhuman)
                    self.labels_valid.append(0)
                except:
                    self.logger.tranceInfo()
                    result_unhuman_valid = False
                    continue
                else:
                    result_unhuman_valid = True

        self.logger.normalInfo('图片数组化')
        self.imgs_train_np = np.array(self.imgs_train)
        self.labels_train_np = tf.one_hot(np.array(self.labels_train), 24)
        self.imgs_valid_np = np.array(self.imgs_valid)
        self.labels_valid_np = tf.one_hot(np.array(self.labels_valid), 24)

        processBar.setValue(55)

        self.logger.varInfo('训练数据及标签')
        self.logger.varInfo(str(self.imgs_train_np) + '\n 形状为\n' + str(self.imgs_train_np.shape))
        self.logger.varInfo(str(self.labels_train_np) + '\n 形状为\n' + str(self.labels_train_np.shape))
        self.logger.varInfo('测试数据及标签')
        self.logger.varInfo(str(self.imgs_valid_np) + '\n 形状为\n' + str(self.imgs_valid_np.shape))
        self.logger.varInfo(str(self.labels_valid_np) + '\n 形状为\n' + str(self.labels_valid_np.shape))

        self.logger.normalInfo('样本及标签数据制作结束')
        return self.imgs_train_np, self.labels_train_np, self.imgs_valid_np, self.labels_valid_np

    def buildModel(self, processBar):
        self.logger.getFuncName('buildModel')
        processBar.setValue(5)
        self.logger.normalInfo('获取数据集')
        imgs_train, labels_train, imgs_valid, labels_valid = self.dataSet_Id(processBar)
        self.obj_GaborBPModel.build(38804)
        processBar.setValue(79)
        self.logger.normalInfo('训练')
        self.obj_GaborBPModel.train(imgs_train, labels_train,
                                    imgs_valid, labels_valid)
        self.logger.normalInfo('训练完毕')
        processBar.setValue(98)
        path_model = os.getcwd()+'\\model\\aggregate.face.model.h5'
        if os.path.exists(path_model):
            os.remove(path_model)
        else:
            os.mkdir(os.getcwd()+'\\model')
        self.logger.normalInfo('构建结束，保存模型')
        self.obj_GaborBPModel.save(os.getcwd()+'\\model\\aggregate.face.model.h5')
        processBar.setValue(100)

    def stopTrain(self):
        self.logger.getFuncName('stopTrain')
        self.logger.normalInfo('中止训练')
        self.obj_GaborBPModel.stop()

    def discriminate(self, path):
        self.logger.getFuncName('discriminate')
        self.logger.normalInfo('进入识别')
        self.logger.normalInfo('导入模型')
        try:
            self.obj_GaborBPModel.load(os.getcwd() + '\\model\\aggregate.face.model.h5')
        except Exception as e:
            self.logger.warringInfo(str(e))
            return None

        self.logger.normalInfo('目标图片预处理')
        img_target = self.obj_imgPre.preFunc(path)
        img_gabored = self.obj_GaborKenel.getGabor(img_target)
        meanImg_target = self.obj_GaborKenel.meanPooling(img_gabored)
        img_target_np = np.array(meanImg_target)
        img_target_reshape = tf.expand_dims(img_target_np, axis=0)
        self.logger.normalInfo('识别')
        try:
            predict = self.obj_GaborBPModel.model.predict(img_target_reshape)
            result = np.argmax(predict[0])
        except:
            self.logger.tranceInfo()
            return 0
        self.logger.varInfo('预测的直接返回值'+str(predict))
        self.logger.varInfo('预测的处理返回值'+str(result))

        self.logger.normalInfo('识别完毕')

        meanImg_target = meanImg_target*255
        return result, img_target, img_gabored, meanImg_target

# 测试函数
def test():
    pass

# 开启动作
if __name__ == '__main__':
    test()
