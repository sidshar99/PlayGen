import sqlite3
import pandas as pd

conn = sqlite3.connect('db.sqlite')

df = pd.read_csv('path/file_name.csv')
df.to_sql('songs', conn, if_exists='append', index=False)
