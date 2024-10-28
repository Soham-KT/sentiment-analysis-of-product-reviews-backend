import tensorflow as tf
import dill as pk
import os


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
        
        model_path = os.path.join(base_dir, 'lstm_model_new.keras')
        self.model = tf.keras.models.load_model(model_path)
        
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