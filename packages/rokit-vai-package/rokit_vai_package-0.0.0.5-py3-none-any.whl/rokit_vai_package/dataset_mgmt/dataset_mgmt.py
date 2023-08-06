from abc import *
import os
import sys

from .. import global_variable as gv
from kfp.v2.components.types.artifact_types import Artifact

#GCP, AWS 등 Cloud storage가 대상
#bucket 생성
#dataset loading
#save dataset to gcs
#save meta to blob 


# pipeline
# PROJECT_ID -> REGION -> PIPELINE_ROOT (PIPELINE_BUCKET_PATH / PIPELINE_NAME) / ID / PIPELINE_DISPLAY_NAME / Pipeline Output
# ex) gs://vertex_ai_rokit_tutorial_lsm/vertex-ai-tutorial-pipeline-lsm/1064916457437/vertex-ai-tutorial-pipeline-lsm-20221110071809/oxford-iiit-pet-load_4365227738282328064
# 
# PROJECT_ID -> REGION -> PIPELINE_TEMPLATE_PATH (PIPELINE_BUCKET_PATH / PIPELINE_FOLDER / PIPELINE_NAME.json)
# ex) vertex_ai_rokit_tutorial_lsm/pipelines/vertex-ai-tutorial-pipeline-lsm.json


# dataset source
# PROJECT_ID -> REGION -> gs://DATASET_BUCKET / original / train / image / file_name.jpg ...
# PROJECT_ID -> REGION -> gs://DATASET_BUCKET / original / train / label / file_name.png ...
# PROJECT_ID -> REGION -> gs://DATASET_BUCKET / original / test / image / file_name.jpg ...
# PROJECT_ID -> REGION -> gs://DATASET_BUCKET / original / test / label / file_name.png ...
# PROJECT_ID -> REGION -> gs://DATASET_BUCKET / label.json
# 
# ex) gs://oxford_iiit_pet_3_2_0/original/train/image/Abyssinian_1.jpg
# 
# label.json : image uri info
# [
#   {
#     "source-ref": "original/train/image/Sphynx_158.jpg",
#     "label-ref": "original/train/label/Sphynx_158.png",
#     "data-type": "train"
#   },
    
    
class DatasetMgmt(Artifact, metaclass=ABCMeta):
    def __init__(self, global_variable, log):
        self.gv = global_variable
        self.log = log
    
    @abstractmethod
    def make_bucket(self, bucket_name):
        pass
    
    @abstractmethod
    def download(self, dataset_name):
        self.log.info(f"{sys._getframe(0).f_code.co_name} function called")
        pass
    
    @abstractmethod
    def upload(self, bucket_name):
        self.log.info(f"{sys._getframe(0).f_code.co_name} function called")
        pass

    @abstractmethod
    def read(self, bucket_name): 
        self.log.info(f"{sys._getframe(0).f_code.co_name} function called")
        pass

    @abstractmethod
    def read_and_split(self, bucket_name, dataset_size, data_split):
        self.log.info(f"{sys._getframe(0).f_code.co_name} function called")
        pass
    
    @abstractmethod
    def write(self, path, dataset): 
        self.log.info(f"{sys._getframe(0).f_code.co_name} function called")
        pass