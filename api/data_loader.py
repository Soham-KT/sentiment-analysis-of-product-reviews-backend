import tensorflow as tf
import dill as pk
import os
import s3fs
from dotenv import load_dotenv
import os

load_dotenv()


AWS_ACCESS_KEY=os.getenv('access_key')
AWS_SECRET_KEY=os.getenv('secret_key')
BUCKET_NAME="testing-public-full-access-bucket"


base_dir = os.path.dirname(__file__)
class ModelLoader:
    _instance = None
    
    @staticmethod
    def get_instance():
        if ModelLoader._instance is None:
            ModelLoader._instance = ModelLoader()
        return ModelLoader._instance
    
    def __init__(self) -> None:
        if ModelLoader._instance is not None:
            raise Exception('This is a singleton')
        
        fs = s3fs.S3FileSystem(key=AWS_ACCESS_KEY, secret=AWS_SECRET_KEY)
        
        for file in fs.ls(BUCKET_NAME):
            if file == 'testing-public-full-access-bucket/lstm_model_new.keras':
                fs.download(file, 'lstm_model.keras')
                break
            
        self.model = tf.keras.models.load_model('lstm_model.keras')
        os.remove('lstm_model.keras')
        
    def get_data(self):
        return self.model
    
    
class TokenizerLoader:
    _instance = None
    
    @staticmethod
    def get_instance():
        if TokenizerLoader._instance is None:
            TokenizerLoader._instance = TokenizerLoader()
        return TokenizerLoader._instance
    
    def __init__(self) -> None:
        if TokenizerLoader._instance is not None:
            raise Exception('This is a singleton')
        
        tokenizer_path = os.path.join(base_dir, 'tokenizer.pkl')
        with open(tokenizer_path, 'rb') as f:
            self.tokenizer = pk.load(f)
        
    def get_data(self):
        return self.tokenizer
    
if __name__ == '__main__':
    tokenizer_path = os.path.join(base_dir, 'tokenizer.pkl')
    model_path = os.path.join(base_dir, 'lstm_model_new.keras')
    
    print(tokenizer_path, model_path)