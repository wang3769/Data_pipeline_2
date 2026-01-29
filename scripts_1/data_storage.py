import os
import sqlite3
import pandas as pd

folder_path = '../data/raw/'

if not os.path.exists(folder_path):
    os.makedirs(folder_path)

os.chdir(folder_path)

#print("Current directory:", os.getcwd())

# Sample: convert articles list to a dataframe first
df = pd.DataFrame(articles)

# Flatten 'source' column (which is a dict)
df['source'] = df['source'].apply(lambda s: s['name'] if isinstance(s, dict) else s)

# Connect to SQLite file (creates if not exist)
conn = sqlite3.connect('news_data.db')

# Save to table called "articles"
df.to_sql('articles', conn, if_exists='append', index=False)

conn.close()