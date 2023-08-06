from PIL import Image
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sb
import os
import warnings

warnings.filterwarnings("ignore")
import tensorflow as tf
from tensorflow.keras.layers.experimental.preprocessing import RandomFlip
import tensorflow.keras.layers as tfl
from tensorflow.keras.preprocessing import image_dataset_from_directory

import keras

from keras import backend as K
from keras.models import Sequential, Model, load_model
from keras.callbacks import EarlyStopping, ModelCheckpoint
from keras.layers import (
    Dropout,
    Input,
    Add,
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
from keras.preprocessing import image
from keras.initializers import glorot_uniform

###########################################################


class LeNetClass(tf.keras.Model):
    def __init__(self, classes=10):
        super(LeNetClass, self).__init__()
        self.conv1 = Conv2D(
            filters=6, kernel_size=(5, 5), padding="same", activation="relu"
        )
        self.max_pool2x2 = MaxPool2D(pool_size=(2, 2))
        self.conv2 = Conv2D(
            filters=16, kernel_size=(5, 5), padding="same", activation="relu"
        )
        self.conv3 = Conv2D(
            filters=120, kernel_size=(5, 5), padding="same", activation="relu"
        )
        self.flatten = Flatten()
        self.fc2 = Dense(units=84, activation="relu")
        self.fc3 = Dense(units=classes, activation="softmax")

    def call(self, inputs):
        # don't create layers here, need to create the layers in initializer,
        # otherwise you will get the tf.Variable can only be created once error
        x = self.conv1(inputs)
        x = self.max_pool2x2(x)
        x = self.conv2(x)
        x = self.max_pool2x2(x)
        x = self.conv3(x)
        x = self.flatten(x)
        x = self.fc2(x)
        x = self.fc3(x)

        return x


###########################################################


def LeNet(classes=10):

    input_layer = Input(shape=(32, 32, 1,))
    x = LeNetClass(classes=classes)(input_layer)
    model = Model(inputs=input_layer, outputs=x)

    return model
