import sys
from prefect import flow, task
import subprocess

@task
def train_model():
    subprocess.run([sys.executable, "train_model_mlflow.py"])

@flow(name="Flipkart Sentiment Training Pipeline")
def sentiment_pipeline():
    train_model()

if __name__ == "__main__":
    sentiment_pipeline()