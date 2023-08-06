Install

pip install tensorflow_image_models==0.0.1

----------------------------------------------

Usage

 from TFIMM import list_models

 list_models()

 models list:  DPN92
               DPN98
               DPN131
               DPN107
               EfficientNetB0
               EfficientNetB1  
               .....
               .....
               VGG16
               VGG19
 
 Create Model

 from TFIMM import EfficientNet

 model=EfficientNet.EfficientNetB0(classes=10)

 model.summary()

----------------------------------------------

License

This project is licensed under the MIT License

----------------------------------------------

Author

DEEPOLOGY LAB
