import sqlite3
import pandas as pd
import os

def setup_database():
    csv_path = os.path.join("ProjFiles", "Document from Pavan.csv")
    db_path = "machine_data.db"
    
    if not os.path.exists(csv_path):
        print(f"Error: Could not find CSV file at {os.path.abspath(csv_path)}")
        return

    print(f"Reading CSV from {csv_path}...")
    try:
        # Read CSV
        df = pd.read_csv(csv_path)
        
        # Ensure DATE_TIME column is treated appropriately if it exists
        if 'DATE_TIME' in df.columns:
            df['DATE_TIME'] = pd.to_datetime(df['DATE_TIME']).dt.strftime('%Y-%m-%d %H:%M:%S')

        # Create SQLite database connection
        conn = sqlite3.connect(db_path)
        
        # Write to database table. The SQL script indicated table name OP10_WELCH_PLUG_PRESS_1
        table_name = "OP10_WELCH_PLUG_PRESS_1"
        df.to_sql(table_name, conn, if_exists="replace", index=False)
        
        print(f"Successfully imported {len(df)} rows into '{table_name}' table in {db_path}")
        conn.close()
    except Exception as e:
        print(f"Error setting up database: {e}")

if __name__ == "__main__":
    setup_database()
