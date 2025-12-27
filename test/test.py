conn = sqlite3.connect(db)

# First check what tables exist
cur = conn.cursor()
cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cur.fetchall()
print('tables:', tables)

# If tables exist, read from the first one
if tables:
    table_name = tables[0][0]
    print(f"\nReading from {table_name}:")
    df = pd.read_sql(f"SELECT * FROM {table_name} LIMIT 10;", conn)
    print(df.head())
else:
    print("\nNo tables found in database!")

conn.close()