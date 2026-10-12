import sqlite3

conn = sqlite3.connect('jomato.db')
cursor = conn.cursor()

print("Task 1: Stored procedure to display restaurant name, type and cuisine where table booking is not zero.")
# Since SQLite doesn't support stored procedures, we'll use a query
cursor.execute("""
SELECT RestaurantName, RestaurantType, CuisinesType
FROM restaurants
WHERE TableBooking != 'No'
""")
results = cursor.fetchall()
print("Results:")
for row in results[:10]:  # Show first 10
    print(row)
print(f"Total rows: {len(results)}\n")

print("Task 2: Create a transaction and update the cuisine type ‘Cafe’ to ‘Cafeteria’. Check the result and rollback it.")
conn.execute("BEGIN TRANSACTION")
cursor.execute("UPDATE restaurants SET CuisinesType = 'Cafeteria' WHERE CuisinesType = 'Cafe'")
cursor.execute("SELECT COUNT(*) FROM restaurants WHERE CuisinesType = 'Cafeteria'")
count = cursor.fetchone()[0]
print(f"Updated {count} rows to 'Cafeteria'")
conn.rollback()
cursor.execute("SELECT COUNT(*) FROM restaurants WHERE CuisinesType = 'Cafeteria'")
count_after = cursor.fetchone()[0]
print(f"After rollback, 'Cafeteria' count: {count_after}\n")

print("Task 3: Generate a row number column and find the top 5 areas with the highest rating of restaurants.")
cursor.execute("""
SELECT Area, AVG(Rating) as AvgRating
FROM restaurants
GROUP BY Area
ORDER BY AvgRating DESC
LIMIT 5
""")
results = cursor.fetchall()
print("Top 5 areas by average rating:")
for row in results:
    print(row)
print()

print("Task 4: Use the while loop to display the 1 to 50.")
i = 1
while i <= 50:
    print(i, end=' ')
    i += 1
print("\n")

print("Task 5: Create a Top rating view to store the generated top 5 highest rating of restaurants.")
cursor.execute("""
CREATE VIEW IF NOT EXISTS TopRatingView AS
SELECT RestaurantName, Rating, Area
FROM restaurants
ORDER BY Rating DESC
LIMIT 5
""")
cursor.execute("SELECT * FROM TopRatingView")
results = cursor.fetchall()
print("Top 5 highest rated restaurants:")
for row in results:
    print(row)
print()

print("Task 6: Create a trigger that gives a message whenever a new record is inserted.")
# SQLite triggers can use RAISE to show messages, but in Python we'll simulate
cursor.execute("""
CREATE TRIGGER IF NOT EXISTS insert_message
AFTER INSERT ON restaurants
BEGIN
    SELECT RAISE(ABORT, 'New record inserted');
END
""")
print("Trigger created. To test, try inserting a record (it will raise an error with message).")

conn.commit()
conn.close()
