import os
import s3fs
import zipfile
import tempfile
import numpy as np
from tensorflow import keras
from pathlib import Path
import logging
from dotenv import load_dotenv

load_dotenv()

AWS_ACCESS_KEY=os.getenv('AWS_ACCESS_KEY')
AWS_SECRET_KEY=os.getenv('AWS_SECRET_KEY')
BUCKET_NAME="testing-public-full-access-bucket"


def get_s3fs():
  return s3fs.S3FileSystem(key=AWS_ACCESS_KEY, secret=AWS_SECRET_KEY)


def zipdir(path, ziph):
  # Zipfile hook to zip up model folders
  length = len(path) # Doing this to get rid of parent folders
  for root, dirs, files in os.walk(path):
    folder = root[length:] # We don't need parent folders! Why in the world does zipfile zip the whole tree??
    for file in files:
      ziph.write(os.path.join(root, file), os.path.join(folder, file))

            
def s3_save_keras_model(model, model_name):
  with tempfile.TemporaryDirectory() as tempdir:
    keras.models.save_model(model, f"{tempdir}/{model_name}.keras")
    # Zip it up first
    zipf = zipfile.ZipFile(f"{tempdir}/{model_name}.zip", "w", zipfile.ZIP_STORED)
    zipdir(f"{tempdir}/{model_name}", zipf)
    zipf.close()
    s3fs = get_s3fs()
    s3fs.put(f"{tempdir}/{model_name}.zip", f"{BUCKET_NAME}/{model_name}.zip")
    logging.info(f"Saved zipped model at path s3://{BUCKET_NAME}/{model_name}.zip")
 

def s3_get_keras_model(model_name: str) -> keras.Model:
  with tempfile.TemporaryDirectory() as tempdir:
    s3fs = get_s3fs()
    # Fetch and save the zip file to the temporary directory
    s3fs.get(f"{BUCKET_NAME}/{model_name}.zip", f"{tempdir}/{model_name}.zip")
    # Extract the model zip file within the temporary directory
    with zipfile.ZipFile(f"{tempdir}/{model_name}.zip") as zip_ref:
        zip_ref.extractall(f"{tempdir}/{model_name}")
    # Load the keras model from the temporary directory
    return keras.models.load_model(f"{tempdir}/{model_name}.keras")
  
  
if __name__ == '__main__':    
    model = keras.models.load_model('lstm_model_new.keras')

    # Save the model to S3
    s3_save_keras_model(model, "my_model") 

    # Load the model from S3
    loaded_model = s3_get_keras_model("my_model")