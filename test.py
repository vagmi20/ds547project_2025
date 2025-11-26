from utils import db
import pandas as pd


conn = db.get_connection()
df = pd.read_sql_query("SELECT * FROM mytable LIMIT 5000;", conn)
print(df.head())