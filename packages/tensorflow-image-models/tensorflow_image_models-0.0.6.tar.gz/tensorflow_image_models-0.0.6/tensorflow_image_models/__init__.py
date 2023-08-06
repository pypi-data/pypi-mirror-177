#from .all_models import list_models
from .DPN import DPN92
from .DPN import DPN98
from .DPN import DPN131
from .DPN import DPN107

from .EfficientNet import EfficientNetB0
from .EfficientNet import EfficientNetB1
from .EfficientNet import EfficientNetB2
from .EfficientNet import EfficientNetB3
from .EfficientNet import EfficientNetB4
from .EfficientNet import EfficientNetB5
from .EfficientNet import EfficientNetB7

from .Inception import InceptionV3
from .Inception import InceptionV4
from .Inception import InceptionResNetV1
from .Inception import InceptionResNetV2

from .LeNet import LeNet

from .Xception import Xception

from .VoVNet import VoVNet27
from .VoVNet import VoVNet39
from .VoVNet import VoVNet57

from .ResNet import ResNet18
from .ResNet import ResNet34
from .ResNet import ResNet50
from .ResNet import ResNet101
from .ResNet import ResNet152

from .MobileNet import MobileNetV1
from .MobileNet import MobileNetV2

from .CspNet import CSPDenseNet

from .AlexNet import AlexNet

from .VGG import VGG16
from .VGG import VGG19

from .DenseNet import DenseNet121
from .DenseNet import DenseNet169
from .DenseNet import DenseNet201

from .ShufflenetV2 import ShufflenetV2

def list_models():
    print(
        "models list:  DPN92 \n DPN98 \n DPN131 \n DPN107",
        "\n EfficientNetB0 \n EfficientNetB1  \n EfficientNetB2 \n EfficientNetB3 \n EfficientNetB4 \n EfficientNetB5 \n EfficientNetB6 \n EfficientNetB7",
        "\n InceptionV3 \n InceptionV4 \n InceptionResNetV1 \n InceptionResNetV2",
        "\n LeNet \n AlexNet",
        "\n Xception",
        "\n VoVNet27 \n VoVNet39 \n VoVNet57",
        "\n CSPDenseNet",
        "\n MobileNetV1 \n MobileNetV2",
        "\n ResNet18 \n ResNet34 \n ResNet50 \n ResNet101 \n ResNet192",
        "\n ShuffleNetV2"
        "\n DenseNet121 \n DenseNet169 \n DenseNet201",
        "\n VGG16 \n VGG19"
    )

    return
