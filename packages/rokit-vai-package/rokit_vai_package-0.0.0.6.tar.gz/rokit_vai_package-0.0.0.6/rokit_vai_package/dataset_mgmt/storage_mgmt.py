import sys
from .. import global_variable as gv
from . import gcp_dataset_mgmt as gcp_dsmgmt
from . import aws_dataset_mgmt as aws_dsmgmt


class Storage():
    
    gv = None
    log = None
    dsmgmt = None
    dsmgmt_module = None
    
    
    def __init__(self, global_variable, log):
        self.gv = global_variable
        self.log = log
        
    def __set_cloud_dataset_mgmt(self, dsmgmt):
        self.dsmgmt_module = dsmgmt
        self.dsmgmt = self.dsmgmt_module.MiddleDatasetMgmt(self.gv, self.log)

        
    def activate_gcp(self):
        self.__set_cloud_dataset_mgmt(gcp_dsmgmt)
        
        
    def activate_aws(self):
        self.__set_cloud_dataset_mgmt(aws_dsmgmt)

        
    ################################################################   
    # Add new cloud activation code in here
    #
    # Example:
    # def activate_new(self):
    #     self.__set_cloud_dataset_mgmt(new_dsmgmt)
    ################################################################
   
        
    def activate_tensorflow_dataset_mgmt(self):
        self.dsmgmt = self.dsmgmt_module.TensorflowDatasetMgmt(self.gv, self.log)
        
        
    def activate_coco_dataset_mgmt(self):
        self.dsmgmt = self.dsmgmt_module.COCODatasetMgmt(self.gv, self.log)

        
    ################################################################   
    # Add new dataset_mgmt activation code in here
    #
    # Example:
    # def activate_new_dataset_mgmt(self):
    #     self.dsmgmt = self.dsmgmt_module.NewDatasetMgmt(self.gv)
    ################################################################

            
    def make_bucket(self, bucket_name):
        self.dsmgmt.make_bucket(bucket_name)
    
    
    def download_upload_dataset(self, dataset_name, bucket_name):
        self.dsmgmt.make_bucket(bucket_name)
        self.dsmgmt.download(dataset_name)
        self.dsmgmt.upload(bucket_name)

        
    def read_and_split_dataset(self, bucket_name, dataset_begin_idx, dataset_size, data_split):
        return self.dsmgmt.read_and_split(bucket_name, dataset_begin_idx, dataset_size, data_split)

        
    def write_dataset(self, path, dataset): 
        self.dsmgmt.write(path, dataset)
        
        
    def read_images(self, path):
        return self.dsmgmt.read_images(path)
    
    
    def augmentation(self, image_dataset):
        return self.dsmgmt.augmente_image(image_dataset)