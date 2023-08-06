Install<br />
pip install tensorflow_image_models==0.0.3

----------------------------------------------

Usage<br />
import tensorflow_image_models as tfimm<br />
from tfimm import list_models<br />
list_models()<br />
models list:<br />
DPN92<br />
DPN98<br />
DPN131<br />
DPN107<br />
EfficientNetB0<br />
EfficientNetB1<br />
.....<br />
.....<br />
VGG16<br />
VGG19<br />
Create Model<br />
from tfimm import EfficientNet<br />
model = EfficientNet.EfficientNetB0(classes=10)<br />
model.summary()

----------------------------------------------

License<br />
This project is licensed under the MIT License

----------------------------------------------

Author<br />
DEEPOLOGY LAB
