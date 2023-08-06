import tensorflow as tf
from tensorflow import keras
from keras.activations import relu
from tensorflow.keras.layers import *
from tensorflow.keras import Model
from tensorflow.keras import layers as Layers
from keras.layers import Dropout, Input


class ResBlock(Model):
    def __init__(self, channels, stride=1):
        super(ResBlock, self).__init__(name="ResBlock")
        self.flag = stride != 1
        self.conv1 = Conv2D(channels, 3, stride, padding="same")
        self.bn1 = BatchNormalization()
        self.conv2 = Conv2D(channels, 3, padding="same")
        self.bn2 = BatchNormalization()
        self.relu = ReLU()
        if self.flag:
            self.bn3 = BatchNormalization()
            self.conv3 = Conv2D(channels, 1, stride)

    def call(self, x):
        x1 = self.conv1(x)
        x1 = self.bn1(x1)
        x1 = self.relu(x1)
        x1 = self.conv2(x1)
        x1 = self.bn2(x1)
        if self.flag:
            x = self.conv3(x)
            x = self.bn3(x)
        x1 = Layers.add([x, x1])
        x1 = self.relu(x1)
        return x1


class ResNet18Class(Model):
    def __init__(self, classes=10):
        super(ResNet18Class, self).__init__(name="ResNet18")
        self.conv1 = Conv2D(64, 7, 2, padding="same")
        self.bn = BatchNormalization()
        self.relu = ReLU()
        self.mp1 = MaxPooling2D(3, 2)

        self.conv2_1 = ResBlock(64)
        self.conv2_2 = ResBlock(64)

        self.conv3_1 = ResBlock(128, 2)
        self.conv3_2 = ResBlock(128)

        self.conv4_1 = ResBlock(256, 2)
        self.conv4_2 = ResBlock(256)

        self.conv5_1 = ResBlock(512, 2)
        self.conv5_2 = ResBlock(512)

        self.pool = GlobalAveragePooling2D()
        self.fc = Dense(classes, activation="softmax")

    def call(self, x):
        x = self.conv1(x)
        x = self.bn(x)
        x = self.relu(x)
        x = self.mp1(x)

        x = self.conv2_1(x)
        x = self.conv2_2(x)

        x = self.conv3_1(x)
        x = self.conv3_2(x)

        x = self.conv4_1(x)
        x = self.conv4_2(x)

        x = self.conv5_1(x)
        x = self.conv5_2(x)

        x = self.pool(x)
        x = self.fc(x)
        return x


def ResNet18(classes=10):
    input_layer = Input(shape=(224, 224, 3,))
    x = ResNet18Class(classes=classes)(input_layer)

    return Model(inputs=input_layer, outputs=x)
