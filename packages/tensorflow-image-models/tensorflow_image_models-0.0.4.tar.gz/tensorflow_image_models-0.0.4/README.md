Install<br />
<br />
pip install tensorflow_image_models==0.0.4

----------------------------------------------

Usage<br />
<br />
import tensorflow_image_models as tfimm<br />
from tfimm import list_models<br />
<br />
list_models()<br />
<br />
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
<br />
Create Model<br />
<br />
from tfimm import EfficientNet<br />
model = EfficientNet.EfficientNetB0(classes=10)<br />
model.summary()
<br />
----------------------------------------------

License<br />
This project is licensed under the MIT License

----------------------------------------------

Author<br />
DEEPOLOGY LAB
