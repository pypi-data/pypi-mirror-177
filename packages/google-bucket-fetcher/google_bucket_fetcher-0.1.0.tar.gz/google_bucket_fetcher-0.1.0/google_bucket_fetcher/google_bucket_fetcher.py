"""Main module."""
#%%

import pandas as pd
from google.cloud import storage
from google.oauth2 import service_account
import json

class GCS:
    
    
    def __init__(self, bucket_name, dataset_name,table,filename, date_extract,extension):
        self.bucket_name = bucket_name
        self.dataset_name = dataset_name
        self.table = table
        self.filename = filename
        self.extension = extension
        self.date_extract = date_extract
        # self.key = key
        # self.project_id = self.key['project_id']
        
    def create_cloudstorage_path(self):

        return f'gs://{self.bucket_name}/{self.dataset_name}/{self.table}/{self.filename}_{self.date_extract}.{self.extension}'
    
    def create_bigquery_path(self):

        return f'{self.dataset_name}.{self.table}'

    def credentials_with_pythondict(self, python_dict):

        credentials = service_account.Credentials.from_service_account_info(python_dict)
        credentials = credentials.with_scopes(
            ['https://www.googleapis.com/auth/cloud-platform'])
        return credentials
    
    def credentials_with_jsonfile(self,path_to_jsonfile):

        credentials = service_account.Credentials.from_service_account_file(path_to_jsonfile)
        credentials = credentials.with_scopes(
            ['https://www.googleapis.com/auth/cloud-platform'])
        return credentials

    def dataframe_tobucket(self,df,path_processed,credentials):
        df.to_csv(path_processed, storage_options={"token": credentials}, index=False)
    
       
    def dataframe_frombucket(self,credentials):
        project_id = credentials.project_id
        storage_client = storage.Client(project=project_id, credentials=credentials)
        processed_data = storage_client.bucket(self.bucket_name)
        my_dataframe_list = []
        df = pd.DataFrame()
        for file in list(processed_data.list_blobs(prefix=f'{self.dataset_name}/{self.table}/')):
            file_path="gs://{}/{}".format(file.bucket.name, file.name)
            print(file_path)
            my_dataframe_list.append(pd.read_csv(file_path, storage_options={"token":credentials}))
            
        df = pd.concat(my_dataframe_list)
        return df
    
    def dataframe_tobigquery(self,df,path,credentials, method='replace'):
        project_id = credentials.project_id
        df.to_gbq(destination_table=path,project_id=project_id,credentials=credentials, if_exists=method)
        return 'table has been sent to bigquery'





#%%