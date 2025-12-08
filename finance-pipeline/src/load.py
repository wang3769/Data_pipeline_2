from sqlalchemy import create_engine
import os

# Ensure a `data` directory exists next to the project root for this package
# `__file__` is `.../src/load.py`, so go up one level to project root and into `data`.
DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'data'))
os.makedirs(DATA_DIR, exist_ok=True)

# Use an absolute path for the SQLite DB inside the `data` folder
DB_PATH = os.path.join(DATA_DIR, 'finance.db')
engine = create_engine(f"sqlite:///{DB_PATH}")

def save_to_db(df, table):
    """
    Save a DataFrame to a SQL database table.

    Parameters:
    df (pandas.DataFrame): The DataFrame to save.
    table (str): The name of the table in the database.
    """
    # Helpful debug info when running the pipeline
    print(f"Saving table '{table}' to database at: {DB_PATH}")
    df.to_sql(table, con=engine, if_exists='replace', index=False)