import pandas as pd
from sqlalchemy import create_engine

# Connect to the SQLite database
engine = create_engine("sqlite+pysqlite:///books.db")

# Read data from the 'books' table
df = pd.read_sql_table('books', engine)

# Check if the 'translated_text' column exists and print it
if 'genere' in df.columns:
    print("Translated Texts:")
    print(df['genere'])
else:
    print("No 'translated_text' column found in the database.")