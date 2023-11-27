### Table of contents
- [General info](#general-info)
  * [Description](#description)
  * [Screenshots](#screenshots)
- [Installation](#installation)
- [Configuration](#configuration)
- [Disclaimer](#disclaimer)


# General info

## Description

TODO

# Configuration
Config file is named `config.ini` and it contains all the changeable settings for the API. Defined parameters are:
* **server** section
  - **host** - host address of the API, default is 127.0.0.1
  - **port** - port of the API, default is 8081
  - **prefix** - prefix of the API, default is "/api/v1"
  - **allow_origins** - list of allowed origins, default is * (all)
  - **allow_methods** - list of allowed origins, default is * (all)
  - **allow_headers** - list of allowed origins, default is * (all)
  - **docs** - enable/disable swagger docs available under `host\port\docs`, default is 1 (on)
  - **redoc** - enable/disable redoc docs available `host\port\redoc`, default is 1 (on)
* **yolo** section
  - **model_weights** - name of the yolov8 to be used, default is yolov8x-cls.pt, make sure to use classifier model (ends with -cls)
  - **img_data_path** - path to the folder with images to be classified, default is ./img_data/
  - **image_threshold** - defines the number of images allowed to exist simultaneously in the yolo predict folder, default is 1000

# Disclaimer
This software does nothing with uploaded data by itself. However, watch out for the fact that ultralytics may use your images for analytics and marketing purposes since their provided package makes post requests to google servers after each model run. 

