import os
import sys
from src.exception import CustomException
from src.logger import logging
import pandas as pd

from sklearn.model_selection import train_test_split
from dataclasses import dataclass
from src.components.data_transformation import DataTransformation
from src.components.data_transformation import DataTransformationConfig
from src.components.model_trainer import ModelTrainer
from src.components.model_trainer import ModelTrainerConfig


@dataclass
class DataIngestionConfig:
    train_test_path: str= os.path.join('artifacts','train.csv')
    test_test_path: str= os.path.join('artifacts','test.csv')
    raw_test_path: str= os.path.join('artifacts','data.csv')

class DataIngestion:
    def __init__(self) -> None:
        self.ingestion_config = DataIngestionConfig()
    
    def initiate_data_ingestion(self):
        
        logging.info("Entered the data ingestion method or component")
        try:
            df = pd.read_csv('notebook\data\stud.csv')
            logging.info("Read the dataset as df")

            os.makedirs(os.path.dirname(self.ingestion_config.train_test_path),exist_ok=True)
            df.to_csv(self.ingestion_config.raw_test_path,index=False,header=True)
            logging.info("Train test split initiated")

            train_set, test_set = train_test_split(df, test_size=0.2, random_state=42)
            train_set.to_csv(self.ingestion_config.train_test_path,index=False,header=True)
            test_set.to_csv(self.ingestion_config.test_test_path,index=False, header=True)

            return(self.ingestion_config.train_test_path,
                   self.ingestion_config.train_test_path)
        except Exception as e:
            raise CustomException(e, sys)
        
if __name__ == "__main__":
    obj = DataIngestion()
    train_data, test_data = obj.initiate_data_ingestion()
    data_transformation = DataTransformation()
    train_arr,test_arr,_= data_transformation.initiate_data_transformation(train_data,test_data)
    modelTrainer = ModelTrainer()
    print(modelTrainer.initiate_model_training(train_arr,test_arr))