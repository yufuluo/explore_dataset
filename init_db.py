import csv
import pandas
import sqlite3

db_dir = './db/'
table_name = 'viewers'

# Import a CSV file into a sqlite3 database table
def csv_to_tb():
    # Create an sqlite connection to a file
    connection = sqlite3.connect(db_dir + 'database.db')
    # Use pandas to read and convert the file
    df = pandas.read_csv(db_dir + 'data.csv')
    df.to_sql(table_name, connection, if_exists='append', index=False)
    # Commit the changes and close the connection
    connection.commit()
    connection.close()

if __name__ == "__main__":
    csv_to_tb()
