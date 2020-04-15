# Contraband Detector App
This app using object detection and a correlation tracker to monitor a frame for items deemed 'contraband'. For working or learning at home, these items may be headphones, cell phones, books, etc. We use two object detection models, to maximize the number of objects we can detect given a set of freely available detection models. You can add or remove models and alter labels to suit your needs!

## Requirements
To run this app, you will need an alwaysAI account. Please register at https://alwaysai.co/auth?register=true

## Setup
Easy start up guides can be found following registration. Please see the docs page for more information: https://alwaysai.co/docs/getting_started/introduction.html

### Models
The object detection models used were the 'alwaysai/ssd_mobilenet_v2_oidv4' model and the 'alwaysai/ssd_inception_v2_coco_2018_01_28' model, and more details can be found at https://alwaysai.co/model-catalog?model=alwaysai/fcn_alexnet_pascal_voc


You can alter the code to used different detection and classification models: https://alwaysai.co/docs/application_development/changing_the_model.html


## Troubleshooting
If you are having trouble connecting to your edge device, use the CLI configure command to reset the device. Please see the following page for more details: https://alwaysai.co/docs/reference/cli_commands.html

You can also post questions and comments on our Discord Community at: https://discord.gg/R2uM36U


