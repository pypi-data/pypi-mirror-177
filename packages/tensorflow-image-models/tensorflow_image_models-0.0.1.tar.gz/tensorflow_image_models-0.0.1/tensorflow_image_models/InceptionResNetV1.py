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
    def __init__(self, filters, kernel_size, strides, padding, activation=True):
        super(ConvBlock, self).__init__()
        self.activation = activation
        self.conv = tf.keras.layers.Conv2D(
            filters=filters, kernel_size=kernel_size, strides=strides, padding=padding
        )
        self.bn = tf.keras.layers.BatchNormalization()

    def call(self, inputs, **kwargs):
        x = self.conv(inputs)
        x = self.bn(x)
        if self.activation == True:
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
        self.maxpool = tf.keras.layers.MaxPool2D(
            pool_size=(3, 3), strides=2, padding="valid"
        )
        self.conv4 = ConvBlock(
            filters=80, kernel_size=(1, 1), strides=1, padding="same"
        )
        self.conv5 = ConvBlock(
            filters=192, kernel_size=(3, 3), strides=1, padding="valid"
        )
        self.conv6 = ConvBlock(
            filters=256, kernel_size=(3, 3), strides=2, padding="valid"
        )

    def call(self, inputs, **kwargs):
        x = self.conv1(inputs)
        x = self.conv2(x)
        x = self.conv3(x)
        x = self.maxpool(x)
        x = self.conv4(x)
        x = self.conv5(x)
        x = self.conv6(x)

        return x


############################################################################


class InceptionResNetA(tf.keras.layers.Layer):
    def __init__(self):
        super(InceptionResNetA, self).__init__()
        self.b1_conv = ConvBlock(
            filters=32, kernel_size=(1, 1), strides=1, padding="same"
        )
        self.b2_conv1 = ConvBlock(
            filters=32, kernel_size=(1, 1), strides=1, padding="same"
        )
        self.b2_conv2 = ConvBlock(
            filters=32, kernel_size=(3, 3), strides=1, padding="same"
        )
        self.b3_conv1 = ConvBlock(
            filters=32, kernel_size=(1, 1), strides=1, padding="same"
        )
        self.b3_conv2 = ConvBlock(
            filters=32, kernel_size=(3, 3), strides=1, padding="same"
        )
        self.b3_conv3 = ConvBlock(
            filters=32, kernel_size=(3, 3), strides=1, padding="same"
        )
        self.conv = ConvBlock(
            filters=256, kernel_size=(1, 1), strides=1, padding="same", activation=False
        )

    def call(self, inputs, **kwargs):
        b1 = self.b1_conv(inputs)
        b2 = self.b2_conv1(inputs)
        b2 = self.b2_conv2(b2)
        b3 = self.b3_conv1(inputs)
        b3 = self.b3_conv2(b3)
        b3 = self.b3_conv3(b3)

        x = tf.concat(values=[b1, b2, b3], axis=-1)
        x = self.conv(x)

        output = tf.keras.layers.add([x, inputs])
        return tf.nn.relu(output)


############################################################################


class ReductionA(tf.keras.layers.Layer):
    def __init__(self, k=192, l=192, m=256, n=384):
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


class InceptionResNetB(tf.keras.layers.Layer):
    def __init__(self):
        super(InceptionResNetB, self).__init__()
        self.b1_conv = ConvBlock(
            filters=128, kernel_size=(1, 1), strides=1, padding="same"
        )
        self.b2_conv1 = ConvBlock(
            filters=128, kernel_size=(1, 1), strides=1, padding="same"
        )
        self.b2_conv2 = ConvBlock(
            filters=128, kernel_size=(1, 7), strides=1, padding="same"
        )
        self.b2_conv3 = ConvBlock(
            filters=128, kernel_size=(7, 1), strides=1, padding="same"
        )
        self.conv = ConvBlock(
            filters=896, kernel_size=(1, 1), strides=1, padding="same", activation=False
        )

    def call(self, inputs, **kwargs):
        b1 = self.b1_conv(inputs)

        b2 = self.b2_conv1(inputs)
        b2 = self.b2_conv2(b2)
        b2 = self.b2_conv3(b2)

        x = tf.concat(values=[b1, b2], axis=-1)
        x = self.conv(x)

        output = tf.keras.layers.add([x, inputs])
        return tf.nn.relu(output)


############################################################################


class ReductionB(tf.keras.layers.Layer):
    def __init__(self):
        super(ReductionB, self).__init__()
        self.b1_maxpool = tf.keras.layers.MaxPool2D(
            pool_size=(3, 3), strides=2, padding="valid"
        )
        self.b2_conv1 = ConvBlock(
            filters=256, kernel_size=(1, 1), strides=1, padding="same"
        )
        self.b2_conv2 = ConvBlock(
            filters=384, kernel_size=(3, 3), strides=2, padding="valid"
        )
        self.b3_conv1 = ConvBlock(
            filters=256, kernel_size=(1, 1), strides=1, padding="same"
        )
        self.b3_conv2 = ConvBlock(
            filters=256, kernel_size=(3, 3), strides=2, padding="valid"
        )
        self.b4_conv1 = ConvBlock(
            filters=256, kernel_size=(1, 1), strides=1, padding="same"
        )
        self.b4_conv2 = ConvBlock(
            filters=256, kernel_size=(3, 3), strides=1, padding="same"
        )
        self.b4_conv3 = ConvBlock(
            filters=256, kernel_size=(3, 3), strides=2, padding="valid"
        )

    def call(self, inputs, **kwargs):
        b1 = self.b1_maxpool(inputs)

        b2 = self.b2_conv1(inputs)
        b2 = self.b2_conv2(b2)

        b3 = self.b3_conv1(inputs)
        b3 = self.b3_conv2(b3)

        b4 = self.b4_conv1(inputs)
        b4 = self.b4_conv2(b4)
        b4 = self.b4_conv3(b4)

        return tf.concat(values=[b1, b2, b3, b4], axis=-1)


############################################################################


class InceptionResNetC(tf.keras.layers.Layer):
    def __init__(self):
        super(InceptionResNetC, self).__init__()
        self.b1_conv = ConvBlock(
            filters=192, kernel_size=(1, 1), strides=1, padding="same"
        )
        self.b2_conv1 = ConvBlock(
            filters=192, kernel_size=(1, 1), strides=1, padding="same"
        )
        self.b2_conv2 = ConvBlock(
            filters=192, kernel_size=(1, 3), strides=1, padding="same"
        )
        self.b2_conv3 = ConvBlock(
            filters=192, kernel_size=(3, 1), strides=1, padding="same"
        )
        self.conv = ConvBlock(
            filters=1792,
            kernel_size=(1, 1),
            strides=1,
            padding="same",
            activation=False,
        )

    def call(self, inputs, **kwargs):
        b1 = self.b1_conv(inputs)
        b2 = self.b2_conv1(inputs)
        b2 = self.b2_conv2(b2)
        b2 = self.b2_conv3(b2)

        x = tf.concat(values=[b1, b2], axis=-1)
        x = self.conv(x)

        output = tf.keras.layers.add([x, inputs])
        return tf.nn.relu(output)


#############################################################################
class InceptionResnetV1Network(tf.keras.Model):
    def __init__(
        self, num_class, resnetA_scale=0.1, resnetB_scale=0.1, resnetC_scale=0.1
    ):

        self.num_class = num_class
        super(InceptionResnetV1Network, self).__init__()
        self.stem = Stem()

        self.inception_resnetA1 = InceptionResNetA()
        self.inception_resnetA2 = InceptionResNetA()
        self.inception_resnetA3 = InceptionResNetA()
        self.inception_resnetA4 = InceptionResNetA()
        self.inception_resnetA5 = InceptionResNetA()

        self.reductionA = ReductionA()

        self.inception_resnetB1 = InceptionResNetB()
        self.inception_resnetB2 = InceptionResNetB()
        self.inception_resnetB3 = InceptionResNetB()
        self.inception_resnetB4 = InceptionResNetB()
        self.inception_resnetB5 = InceptionResNetB()
        self.inception_resnetB6 = InceptionResNetB()
        self.inception_resnetB7 = InceptionResNetB()
        self.inception_resnetB8 = InceptionResNetB()
        self.inception_resnetB9 = InceptionResNetB()
        self.inception_resnetB10 = InceptionResNetB()

        self.reductionB = ReductionB()

        self.inception_resnetC1 = InceptionResNetC()
        self.inception_resnetC2 = InceptionResNetC()
        self.inception_resnetC3 = InceptionResNetC()
        self.inception_resnetC4 = InceptionResNetC()
        self.inception_resnetC5 = InceptionResNetC()

        self.average_pool = GlobalAveragePooling2D()
        self.dropout = Dropout(rate=0.2)
        self.classifier = Dense(self.num_class, activation="softmax")

    def call(self, input):
        stem_out = self.stem(input)
        inception_resnetA1_out = self.inception_resnetA1(stem_out)
        inception_resnetA2_out = self.inception_resnetA2(inception_resnetA1_out)
        inception_resnetA3_out = self.inception_resnetA3(inception_resnetA2_out)
        inception_resnetA4_out = self.inception_resnetA4(inception_resnetA3_out)
        inception_resnetA5_out = self.inception_resnetA5(inception_resnetA4_out)

        reductionA_out = self.reductionA(inception_resnetA5_out)

        inception_resnetB1_out = self.inception_resnetB1(reductionA_out)
        inception_resnetB2_out = self.inception_resnetB2(inception_resnetB1_out)
        inception_resnetB3_out = self.inception_resnetB3(inception_resnetB2_out)
        inception_resnetB4_out = self.inception_resnetB4(inception_resnetB3_out)
        inception_resnetB5_out = self.inception_resnetB5(inception_resnetB4_out)
        inception_resnetB6_out = self.inception_resnetB6(inception_resnetB5_out)
        inception_resnetB7_out = self.inception_resnetB7(inception_resnetB6_out)
        inception_resnetB8_out = self.inception_resnetB8(inception_resnetB7_out)
        inception_resnetB9_out = self.inception_resnetB9(inception_resnetB8_out)
        inception_resnetB10_out = self.inception_resnetB10(inception_resnetB9_out)

        reductionB_out = self.reductionB(inception_resnetB10_out)

        inception_resnetC1_out = self.inception_resnetC1(reductionB_out)
        inception_resnetC2_out = self.inception_resnetC2(inception_resnetC1_out)
        inception_resnetC3_out = self.inception_resnetC3(inception_resnetC2_out)
        inception_resnetC4_out = self.inception_resnetC4(inception_resnetC3_out)
        inception_resnetC5_out = self.inception_resnetC5(inception_resnetC4_out)

        average_pool_out = self.average_pool(inception_resnetC5_out)
        drop_out = self.dropout(average_pool_out)
        prob_out = self.classifier(drop_out)

        return prob_out


############################################################################
        
def build_graph(self, raw_shape):
    x = tf.keras.layers.Input(shape=raw_shape)
    return Model(inputs=[x], outputs=self.call(x))


############################################################################


def InceptionResNetV1(classes=10):
    input_layer = Input(shape=(128, 128, 3,))
    x = InceptionResnetV1Network(num_class=classes)(input_layer)

    return Model(inputs=input_layer, outputs=x)
