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
from tensorflow.keras.preprocessing import image
from tensorflow.keras.initializers import glorot_uniform

# Model Checks
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score
from sklearn.metrics import roc_auc_score


import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelBinarizer
from sklearn.metrics import roc_curve, auc, roc_auc_score
from itertools import cycle

# Model Graphs
from sklearn.metrics import confusion_matrix
from sklearn.metrics import ConfusionMatrixDisplay
from keras.layers import Activation, Lambda, GlobalAveragePooling2D, concatenate
import math
from tensorflow.keras.layers import DepthwiseConv2D
from keras.layers import SeparableConv2D, Add, GlobalAvgPool2D
from keras.layers import Resizing
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import tensorflow_addons as tfa


class ConvBlock(tf.keras.layers.Layer):
    def __init__(self, filters, kernel_size, strides, padding):
        super(ConvBlock, self).__init__()
        self.conv = tf.keras.layers.Conv2D(
            filters=filters, kernel_size=kernel_size, strides=strides, padding=padding
        )
        self.bn = tf.keras.layers.BatchNormalization()

    def call(self, inputs, training=None, **kwargs):
        x = self.conv(inputs)
        x = self.bn(x, training=training)
        x = tf.nn.relu(x)

        return x


############################################################################


class Stem(tf.keras.layers.Layer):
    def __init__(self):
        super(Stem, self).__init__()
        self.conv1 = ConvBlock(
            filters=32, kernel_size=(3, 3), strides=2, padding="valid"
        )
        self.conv2 = ConvBlock(
            filters=32, kernel_size=(3, 3), strides=1, padding="valid"
        )
        self.conv3 = ConvBlock(
            filters=64, kernel_size=(3, 3), strides=1, padding="same"
        )
        self.b1_maxpool = tf.keras.layers.MaxPool2D(
            pool_size=(3, 3), strides=2, padding="valid"
        )
        self.b2_conv = ConvBlock(
            filters=96, kernel_size=(3, 3), strides=2, padding="valid"
        )
        self.b3_conv1 = ConvBlock(
            filters=64, kernel_size=(1, 1), strides=1, padding="same"
        )
        self.b3_conv2 = ConvBlock(
            filters=96, kernel_size=(3, 3), strides=1, padding="valid"
        )
        self.b4_conv1 = ConvBlock(
            filters=64, kernel_size=(1, 1), strides=1, padding="same"
        )
        self.b4_conv2 = ConvBlock(
            filters=64, kernel_size=(7, 1), strides=1, padding="same"
        )
        self.b4_conv3 = ConvBlock(
            filters=64, kernel_size=(1, 7), strides=1, padding="same"
        )
        self.b4_conv4 = ConvBlock(
            filters=96, kernel_size=(3, 3), strides=1, padding="valid"
        )
        self.b5_conv = ConvBlock(
            filters=192, kernel_size=(3, 3), strides=2, padding="valid"
        )
        self.b6_maxpool = tf.keras.layers.MaxPool2D(
            pool_size=(3, 3), strides=2, padding="valid"
        )

    def call(self, inputs, **kwargs):
        x = self.conv1(inputs)
        x = self.conv2(x)
        x = self.conv3(x)
        branch_1 = self.b1_maxpool(x)
        branch_2 = self.b2_conv(x)
        x = tf.concat(values=[branch_1, branch_2], axis=-1)
        branch_3 = self.b3_conv1(x)
        branch_3 = self.b3_conv2(branch_3)
        branch_4 = self.b4_conv1(x)
        branch_4 = self.b4_conv2(branch_4)
        branch_4 = self.b4_conv3(branch_4)
        branch_4 = self.b4_conv4(branch_4)
        x = tf.concat(values=[branch_3, branch_4], axis=-1)
        branch_5 = self.b5_conv(x)
        branch_6 = self.b6_maxpool(x)
        x = tf.concat(values=[branch_5, branch_6], axis=-1)

        return x


############################################################################


class InceptionBlockA(tf.keras.layers.Layer):
    def __init__(self):
        super(InceptionBlockA, self).__init__()
        self.b1_pool = tf.keras.layers.AveragePooling2D(
            pool_size=(3, 3), strides=1, padding="same"
        )
        self.b1_conv = ConvBlock(
            filters=96, kernel_size=(1, 1), strides=1, padding="same"
        )
        self.b2_conv = ConvBlock(
            filters=96, kernel_size=(1, 1), strides=1, padding="same"
        )
        self.b3_conv1 = ConvBlock(
            filters=64, kernel_size=(1, 1), strides=1, padding="same"
        )
        self.b3_conv2 = ConvBlock(
            filters=96, kernel_size=(3, 3), strides=1, padding="same"
        )
        self.b4_conv1 = ConvBlock(
            filters=64, kernel_size=(1, 1), strides=1, padding="same"
        )
        self.b4_conv2 = ConvBlock(
            filters=96, kernel_size=(3, 3), strides=1, padding="same"
        )
        self.b4_conv3 = ConvBlock(
            filters=96, kernel_size=(3, 3), strides=1, padding="same"
        )

    def call(self, inputs, **kwargs):
        b1 = self.b1_pool(inputs)
        b1 = self.b1_conv(b1)

        b2 = self.b2_conv(inputs)

        b3 = self.b3_conv1(inputs)
        b3 = self.b3_conv2(b3)

        b4 = self.b4_conv1(inputs)
        b4 = self.b4_conv2(b4)
        b4 = self.b4_conv3(b4)

        return tf.concat(values=[b1, b2, b3, b4], axis=-1)


############################################################################


class ReductionA(tf.keras.layers.Layer):
    def __init__(self, k=192, l=224, m=256, n=384):
        super(ReductionA, self).__init__()
        self.b1_pool = tf.keras.layers.MaxPool2D(
            pool_size=(3, 3), strides=2, padding="valid"
        )
        self.b2_conv = ConvBlock(
            filters=n, kernel_size=(3, 3), strides=2, padding="valid"
        )
        self.b3_conv1 = ConvBlock(
            filters=k, kernel_size=(1, 1), strides=1, padding="same"
        )
        self.b3_conv2 = ConvBlock(
            filters=l, kernel_size=(3, 3), strides=1, padding="same"
        )
        self.b3_conv3 = ConvBlock(
            filters=m, kernel_size=(3, 3), strides=2, padding="valid"
        )

    def call(self, inputs, **kwargs):
        b1 = self.b1_pool(inputs)

        b2 = self.b2_conv(inputs)

        b3 = self.b3_conv1(inputs)
        b3 = self.b3_conv2(b3)
        b3 = self.b3_conv3(b3)

        return tf.concat(values=[b1, b2, b3], axis=-1)


############################################################################


class InceptionBlockB(tf.keras.layers.Layer):
    def __init__(self):
        super(InceptionBlockB, self).__init__()
        self.b1_pool = tf.keras.layers.AveragePooling2D(
            pool_size=(3, 3), strides=1, padding="same"
        )
        self.b1_conv = ConvBlock(
            filters=128, kernel_size=(1, 1), strides=1, padding="same"
        )
        self.b2_conv = ConvBlock(
            filters=384, kernel_size=(1, 1), strides=1, padding="same"
        )
        self.b3_conv1 = ConvBlock(
            filters=192, kernel_size=(1, 1), strides=1, padding="same"
        )
        self.b3_conv2 = ConvBlock(
            filters=224, kernel_size=(1, 7), strides=1, padding="same"
        )
        self.b3_conv3 = ConvBlock(
            filters=256, kernel_size=(1, 7), strides=1, padding="same"
        )
        self.b4_conv1 = ConvBlock(
            filters=192, kernel_size=(1, 1), strides=1, padding="same"
        )
        self.b4_conv2 = ConvBlock(
            filters=192, kernel_size=(1, 7), strides=1, padding="same"
        )
        self.b4_conv3 = ConvBlock(
            filters=224, kernel_size=(7, 1), strides=1, padding="same"
        )
        self.b4_conv4 = ConvBlock(
            filters=224, kernel_size=(1, 7), strides=1, padding="same"
        )
        self.b4_conv5 = ConvBlock(
            filters=256, kernel_size=(7, 1), strides=1, padding="same"
        )

    def call(self, inputs, **kwargs):
        b1 = self.b1_pool(inputs)
        b1 = self.b1_conv(b1)

        b2 = self.b2_conv(inputs)

        b3 = self.b3_conv1(inputs)
        b3 = self.b3_conv2(b3)
        b3 = self.b3_conv3(b3)

        b4 = self.b4_conv1(inputs)
        b4 = self.b4_conv2(b4)
        b4 = self.b4_conv3(b4)
        b4 = self.b4_conv4(b4)
        b4 = self.b4_conv5(b4)

        return tf.concat(values=[b1, b2, b3, b4], axis=-1)


############################################################################


class ReductionB(tf.keras.layers.Layer):
    def __init__(self):
        super(ReductionB, self).__init__()
        self.b1_pool = tf.keras.layers.MaxPool2D(
            pool_size=(3, 3), strides=2, padding="valid"
        )
        self.b2_conv1 = ConvBlock(
            filters=192, kernel_size=(1, 1), strides=1, padding="same"
        )
        self.b2_conv2 = ConvBlock(
            filters=192, kernel_size=(3, 3), strides=2, padding="valid"
        )
        self.b3_conv1 = ConvBlock(
            filters=256, kernel_size=(1, 1), strides=1, padding="same"
        )
        self.b3_conv2 = ConvBlock(
            filters=256, kernel_size=(1, 7), strides=1, padding="same"
        )
        self.b3_conv3 = ConvBlock(
            filters=320, kernel_size=(7, 1), strides=1, padding="same"
        )
        self.b3_conv4 = ConvBlock(
            filters=320, kernel_size=(3, 3), strides=2, padding="valid"
        )

    def call(self, inputs, **kwargs):
        b1 = self.b1_pool(inputs)

        b2 = self.b2_conv1(inputs)
        b2 = self.b2_conv2(b2)

        b3 = self.b3_conv1(inputs)
        b3 = self.b3_conv2(b3)
        b3 = self.b3_conv3(b3)
        b3 = self.b3_conv4(b3)

        return tf.concat(values=[b1, b2, b3], axis=-1)


############################################################################


class InceptionBlockC(tf.keras.layers.Layer):
    def __init__(self):
        super(InceptionBlockC, self).__init__()
        self.b1_pool = tf.keras.layers.AveragePooling2D(
            pool_size=(3, 3), strides=1, padding="same"
        )
        self.b1_conv = ConvBlock(
            filters=256, kernel_size=(1, 1), strides=1, padding="same"
        )
        self.b2_conv = ConvBlock(
            filters=256, kernel_size=(1, 1), strides=1, padding="same"
        )
        self.b3_conv1 = ConvBlock(
            filters=384, kernel_size=(1, 1), strides=1, padding="same"
        )
        self.b3_conv2 = ConvBlock(
            filters=256, kernel_size=(1, 3), strides=1, padding="same"
        )
        self.b3_conv3 = ConvBlock(
            filters=256, kernel_size=(3, 1), strides=1, padding="same"
        )
        self.b4_conv1 = ConvBlock(
            filters=384, kernel_size=(1, 1), strides=1, padding="same"
        )
        self.b4_conv2 = ConvBlock(
            filters=448, kernel_size=(1, 3), strides=1, padding="same"
        )
        self.b4_conv3 = ConvBlock(
            filters=512, kernel_size=(3, 1), strides=1, padding="same"
        )
        self.b4_conv4 = ConvBlock(
            filters=256, kernel_size=(3, 1), strides=1, padding="same"
        )
        self.b4_conv5 = ConvBlock(
            filters=256, kernel_size=(1, 3), strides=1, padding="same"
        )

    def call(self, inputs, **kwargs):
        b1 = self.b1_pool(inputs)
        b1 = self.b1_conv(b1)

        b2 = self.b2_conv(inputs)

        b3 = self.b3_conv1(inputs)
        b3_1 = self.b3_conv2(b3)
        b3_2 = self.b3_conv3(b3)

        b4 = self.b4_conv1(inputs)
        b4 = self.b4_conv2(b4)
        b4 = self.b4_conv3(b4)
        b4_1 = self.b4_conv4(b4)
        b4_2 = self.b4_conv5(b4)

        return tf.concat(values=[b1, b2, b3_1, b3_2, b4_1, b4_2], axis=-1)


###########################################################################


class InceptionV4Network(tf.keras.Model):
    def __init__(
        self, classes=10, resnetA_scale=0.1, resnetB_scale=0.1, resnetC_scale=0.1
    ):

        super(InceptionV4Network, self).__init__()
        self.stem = Stem()

        self.inception_A1 = InceptionBlockA()
        self.inception_A2 = InceptionBlockA()
        self.inception_A3 = InceptionBlockA()
        self.inception_A4 = InceptionBlockA()

        self.reductionA = ReductionA()

        self.inception_B1 = InceptionBlockB()
        self.inception_B2 = InceptionBlockB()
        self.inception_B3 = InceptionBlockB()
        self.inception_B4 = InceptionBlockB()
        self.inception_B5 = InceptionBlockB()
        self.inception_B6 = InceptionBlockB()
        self.inception_B7 = InceptionBlockB()

        self.reductionB = ReductionB()

        self.inception_C1 = InceptionBlockC()
        self.inception_C2 = InceptionBlockC()
        self.inception_C3 = InceptionBlockC()

        self.average_pool = GlobalAveragePooling2D()
        self.dropout = Dropout(rate=0.2)
        self.classifier = Dense(classes, activation="softmax")

    def call(self, input):
        stem_out = self.stem(input)
        inception_A1_out = self.inception_A1(stem_out)
        inception_A2_out = self.inception_A2(inception_A1_out)
        inception_A3_out = self.inception_A3(inception_A2_out)
        inception_A4_out = self.inception_A4(inception_A3_out)

        reductionA_out = self.reductionA(inception_A4_out)

        inception_B1_out = self.inception_B1(reductionA_out)
        inception_B2_out = self.inception_B2(inception_B1_out)
        inception_B3_out = self.inception_B3(inception_B2_out)
        inception_B4_out = self.inception_B4(inception_B3_out)
        inception_B5_out = self.inception_B5(inception_B4_out)
        inception_B6_out = self.inception_B6(inception_B5_out)
        inception_B7_out = self.inception_B7(inception_B6_out)

        reductionB_out = self.reductionB(inception_B7_out)

        inception_C1_out = self.inception_C1(reductionB_out)
        inception_C2_out = self.inception_C2(inception_C1_out)
        inception_C3_out = self.inception_C3(inception_C2_out)

        x = self.average_pool(inception_C3_out)
        x = self.dropout(x)
        prob_out = self.classifier(x)

        return prob_out


############################################################################


def build_graph(self, raw_shape):
    x = tf.keras.layers.Input(shape=raw_shape)
    return Model(inputs=[x], outputs=self.call(x))


###########################################################################
    
def InceptionV4(classes=10):
    input_layer = Input(shape=(128, 128, 3,))
    x = InceptionV4Network(classes=classes)(input_layer)

    return Model(inputs=input_layer, outputs=x)
