from transformers import pipeline

from transformers import AutoModelForCausalLM, AutoTokenizer

import sqlite3
import pandas as pd
import os

# local_dir = "../models/tinyllama-chat" # if you running locally
# tokenizer = AutoTokenizer.from_pretrained(local_dir)
# model = AutoModelForCausalLM.from_pretrained(local_dir)

airflow_dir = "/opt/airflow/models/tinyllama-chat" # if you running locally
tokenizer = AutoTokenizer.from_pretrained(airflow_dir)
model = AutoModelForCausalLM.from_pretrained(airflow_dir)

generator = pipeline("text-generation", model=model, tokenizer=tokenizer)

#Input to trick tinnyllama into summarization
folder_path = "/opt/airflow/data/"

if not os.path.exists(folder_path):
    os.makedirs(folder_path)

os.chdir(folder_path)

#conn = sqlite3.connect('../data/raw/news_data.db') #if you are running locally
conn = sqlite3.connect('news_data.db')  # if you are running in Airflow

# Save to table called "articles"
df = pd.read_sql("SELECT * FROM articles LIMIT 10;", conn)
print(df.head())

conn.close()

news_text = " ".join(df['title'].dropna())

input_text = "Summarize the following text: " + news_text

# Run inference
output = generator(input_text, max_new_tokens=100)
print(output[0]['generated_text'])