import sqlite3
import os
import pandas as pd
#from wordcloud import WordCloud


#folder_path = '../data/raw/'
folder_path = "/opt/airflow/data/"

if not os.path.exists(folder_path):
    os.makedirs(folder_path)

os.chdir(folder_path)

conn = sqlite3.connect('news_data.db')

# Save to table called "articles"
df = pd.read_sql("SELECT * FROM articles", conn)
print(df.head())

conn.close()

# text = " ".join(df['title'].dropna())
# wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)

# plt.figure(figsize=(10, 5))
# plt.imshow(wordcloud, interpolation='bilinear')
# plt.axis('off')
# plt.title("Word Cloud of News Titles")
# plt.show()