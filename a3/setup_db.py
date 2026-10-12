import sqlite3
import pandas as pd

# Connect to SQLite database (creates if doesn't exist)
conn = sqlite3.connect('jomato.db')
cursor = conn.cursor()

# Read and execute the create table SQL
with open('create_table.sql', 'r') as f:
    sql = f.read()
cursor.execute(sql)

# Import CSV data using pandas
df = pd.read_csv('Jomato.csv')
df.columns = ['OrderId', 'RestaurantName', 'RestaurantType', 'Rating', 'NoOfRating', 'AverageCost', 'OnlineOrder', 'TableBooking', 'CuisinesType', 'Area', 'LocalAddress', 'DeliveryTime']
df.to_sql('restaurants', conn, if_exists='append', index=False)

conn.commit()
print("Database setup complete. Table created and data imported.")
