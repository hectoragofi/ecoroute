import sqlite3
import pandas as pd

# Read the CSV file into a Pandas DataFrame
csv_file_path = 'ports.csv'  # Replace with the actual path to your CSV file
df = pd.read_csv(csv_file_path)

# Connect to SQLite database (this will create a new file if it doesn't exist)
db_path = 'ports.db'  # Replace with the desired path for your SQLite database
conn = sqlite3.connect(db_path)

# Write the DataFrame to the SQLite database
df.to_sql('ports', conn, index=False, if_exists='replace')

# Commit the changes and close the connection
conn.commit()
conn.close()
