from utils import db
import pandas as pd


db.setup_database("data/song_lyrics_subset.csv")
conn = db.get_connection()
# df = pd.read_sql_query("SELECT * FROM mytable LIMIT 5000;", conn)
# print(df.head())

ranked = db.bm25("love")
# print(ranked.head())

print(db.query("happy songs from the nineties", artist="Kanye West", language="en"))