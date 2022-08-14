# python包
import tensorflow as tf
import os
import math
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# 自建包
from CodeTools.loggingTool import GaborLogger

#类
class GaborBPNetModel():
    def __init__(self):
        self.logger = GaborLogger('GaborBPNetModel')
        self.model = None

    def build(self, num_input):
        num_hidden = math.isqrt(num_input+1)
        self.logger.varInfo('隐藏层为维数为->'+str(num_hidden))
        self.logger.getFuncName('build')
        self.logger.normalInfo('生成网络对象——model')
        self.model = tf.keras.models.Sequential()
        self.logger.normalInfo('输入层')
        self.model.add(tf.keras.layers.Flatten(input_shape=(218, 178, 3)))  # 拉直层
        self.logger.normalInfo('隐藏层H1')
        self.model.add(tf.keras.layers.Dense(num_hidden, activation='relu'))  # 隐藏层H1
        self.logger.normalInfo('隐藏层H2')
        self.model.add(tf.keras.layers.Dense(num_hidden, activation='relu'))  # 隐藏层H2
        """
        self.logger.normalInfo('隐藏层H3')
        self.model.add(tf.keras.layers.Dense())  # 隐藏层H3
        """
        self.logger.normalInfo('输出层')
        self.model.add(tf.keras.layers.Dense(24))  # 输出层
        self.model.add(tf.keras.layers.Activation('softmax'))

        self.model.summary()

    def train(self, imgs_train, labels_train, imgs_valid, labels_valid):
        self.logger.getFuncName('train')
        self.logger.normalInfo('设置训练参数')
        STEPS_PER_EPOCH = int(1e4)//32
        lr_schedule = tf.keras.optimizers.schedules.InverseTimeDecay(
            0.001,
            decay_steps=STEPS_PER_EPOCH * 1000,
            decay_rate=1,
            staircase=False)
        optimizer = tf.keras.optimizers.Adam(lr_schedule)
        self.model.compile(loss='categorical_crossentropy', optimizer=optimizer, metrics=['accuracy'])
        self.model.fit(imgs_train, labels_train, batch_size=32, epochs=20,
                       validation_data=(imgs_valid, labels_valid))

    def save(self, path_netModel):
        self.logger.getFuncName('save')
        self.logger.normalInfo('保存模型')
        self.logger.normalInfo('路径为->' + str(path_netModel))
        self.model.save(path_netModel)

    def load(self, path_netModel):
        self.logger.getFuncName('load')
        self.logger.normalInfo('导入模型')
        self.logger.normalInfo('路径为->' + str(path_netModel))
        self.model = tf.keras.models.load_model(path_netModel)

    def stop(self):
        self.logger.getFuncName('stop')
        self.logger.normalInfo('中止训练')
        early_stopping = tf.keras.callbacks.EarlyStopping(monitor='val_loss', min_delta=0,
                                                          patience=0, verbose=0, mode='auto',
                                                          baseline=None, restore_best_weights=False)
        self.model.fit(callbacks=[early_stopping])
        self.logger.normalInfo('训练已结束')

#测试函数
def test():
    pass

#开启动作
if __name__ == '__main__':
    test()
