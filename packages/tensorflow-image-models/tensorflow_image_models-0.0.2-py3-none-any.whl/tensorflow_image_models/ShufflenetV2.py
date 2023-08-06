import keras
import numpy as np
import tensorflow as tf

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sb
import os
import warnings

warnings.filterwarnings("ignore")
import tensorflow as tf
from tensorflow.keras.layers.experimental.preprocessing import RandomFlip
from tensorflow.keras.layers import DepthwiseConv2D, Layer
from tensorflow.keras import layers
from tensorflow.keras.preprocessing import image_dataset_from_directory


import keras

from tensorflow.keras import backend as K
from tensorflow.keras.models import Sequential, Model, load_model
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from tensorflow.keras.layers import (
    Dropout,
    ReLU,
    Layer,
    Input,
    add,
    Dense,
    Activation,
    ZeroPadding2D,
    BatchNormalization,
    Flatten,
    Conv2D,
    AveragePooling2D,
    MaxPooling2D,
    GlobalMaxPooling2D,
    MaxPool2D,
)

import tensorflow 
import tensorflow  as tf
import os

def batch_norm(training):
    return layers.BatchNormalization(axis=3, momentum=0.99,
                        epsilon=0.001, center=True,
                        scale=True, trainable=training, fused=True)


class ShufflenetV2Class(Model):
    def __init__(self, classes=10, training=False):
        super(ShufflenetV2Class, self).__init__()

        self.training = training

        self.conv1 = layers.Conv2D(24, kernel_size=3, strides=2, padding='SAME')
        self.bn1 = batch_norm(self.training)
        self.act1 = layers.Activation("relu")
        self.maxpool1 = layers.MaxPooling2D((3, 3), (2, 2), padding='SAME')

        self.block1 = ShuffleBlock(num_units=4, in_channels = 24, out_channels = 116)
        self.block2 = ShuffleBlock(num_units=8, in_channels = 116)
        self.block3 = ShuffleBlock(num_units=4, in_channels = 232)

        self.globalavgpool = layers.GlobalAveragePooling2D()
        self.dense1 = layers.Dense(classes,activation='softmax')

        self.conv5 = layers.Conv2D(1024, kernel_size=1, strides=1, padding='SAME')
        self.bn5 = batch_norm(self.training)
        self.act5 = layers.Activation("relu")




    def call(self, inputs):
        x = self.conv1(inputs)
        x = self.bn1(x)
        x = self.act1(x)
        x = self.maxpool1(x)

        x = self.block1(x)
        x = self.block2(x)
        x = self.block3(x)

        x = self.conv5(x)
        x = self.bn5(x)
        x = self.act5(x)

        x = self.globalavgpool(x)
        x = self.dense1(x)

        return x

class ShuffleBlock(tf.keras.layers.Layer):
    def __init__(self, num_units, in_channels, out_channels=None, training=True):
        super(ShuffleBlock, self).__init__()

        self.training = training
        self.num_units = num_units
        self.in_channels = in_channels
        self.out_channels = 2 * self.in_channels if out_channels is None else out_channels

        self.all_basic_uint = []
        for j in range(2, self.num_units + 1):
            self.all_basic_uint.append(BasicUnit(in_channels=self.out_channels//2))


        self.conv1 = layers.Conv2D(self.in_channels, kernel_size=1, strides=1, padding='SAME')
        self.bn1 = batch_norm(self.training)
        self.act1 = layers.Activation("relu")

        self.dwconv2 = layers.DepthwiseConv2D(kernel_size=3, strides=2, padding='SAME') 
        self.bn2 = batch_norm(self.training)
       
        self.conv3 = layers.Conv2D(self.out_channels // 2, kernel_size=1,strides=1, padding='SAME')
        self.bn3 = batch_norm(self.training)
        self.act3 = layers.Activation("relu")

        self.dwconv4 = layers.DepthwiseConv2D(kernel_size=3, strides=2, padding='SAME')
        self.bn4 = batch_norm(self.training)

        self.conv5 = layers.Conv2D(self.out_channels // 2, kernel_size=1,strides=1, padding='SAME')
        self.bn5 = batch_norm(self.training)
        self.act5 = layers.Activation("relu")
        

    def shuffle_xy(self, x, y):
        
        batch_size, height, width, channels = x.shape[:]
        depth = channels
        z = tf.stack([x, y], axis=3)
        z = tf.transpose(z, [0, 1, 2, 4, 3])
        z = tf.reshape(z, [-1, height, width, 2*depth]) 
        x, y = tf.split(z, num_or_size_splits=2, axis=3)
        return x, y


    def call(self, x):
        y = self.conv1(x)
        y = self.bn1(y)
        y = self.act1(y)

        y = self.dwconv2(y)
        y = self.bn2(y)

        y = self.conv3(y)
        y = self.bn3(y)
        y = self.act3(y)

        x = self.dwconv4(x)
        x = self.bn4(x)

        x = self.conv5(x)
        x = self.bn5(x)
        x = self.act5(x)

        basic_uint_count = 0
        for j in range(2, self.num_units + 1):
            x, y = self.shuffle_xy(x, y)
            x = self.all_basic_uint[basic_uint_count](x)
            basic_uint_count += 1

        x = layers.concatenate([x,y])
        return x

class BasicUnit(tf.keras.layers.Layer):
    def __init__(self, in_channels = 10, training = True):
        super(BasicUnit, self).__init__()
        self.in_channels = in_channels

        self.training = training
        self.conv1 = layers.Conv2D(self.in_channels, kernel_size=1, strides=1, padding='SAME')
        self.bn1 = batch_norm(self.training)
        self.act1 = layers.Activation("relu")

        self.dwconv2 = layers.DepthwiseConv2D(kernel_size=3, strides=1, padding='SAME') 
        self.bn2 = batch_norm(self.training)

        self.conv3 = layers.Conv2D(self.in_channels, kernel_size=1, strides=1, padding='SAME')
        self.bn3 = batch_norm(self.training)
        self.act3 = layers.Activation("relu")


    def call(self, x):
        x = self.conv1(x)
        x = self.bn1(x)
        x = self.act1(x)

        x = self.dwconv2(x)
        x = self.bn2(x)

        x = self.conv3(x)
        x = self.bn3(x)
        x = self.act3(x)
        return x

def ShufflenetV2(classes=10):

    inputs=Input(shape=(128,128,3))
    model=ShufflenetV2Class(classes=classes,training=False)(inputs)
    model = Model(inputs=inputs, outputs= model)

    return model










