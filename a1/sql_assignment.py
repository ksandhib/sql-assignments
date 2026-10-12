import sqlite3

# Connect to SQLite database (creates if doesn't exist)
conn = sqlite3.connect('abc_fashion.db')
cursor = conn.cursor()

# Create Salesman table
cursor.execute('''
CREATE TABLE Salesman (
    SalesmanId INT,
    Name VARCHAR(255),
    Commission DECIMAL(10,2),
    City VARCHAR(255),
    Age INT
)
''')

# Insert data into Salesman
salesman_data = [
    (101, 'Joe', 50, 'California', 17),
    (102, 'Simon', 75, 'Texas', 25),
    (103, 'Jessie', 105, 'Florida', 35),
    (104, 'Danny', 100, 'Texas', 22),
    (105, 'Lia', 65, 'NewJersey', 30)
]
cursor.executemany('INSERT INTO Salesman VALUES (?, ?, ?, ?, ?)', salesman_data)

# Create Customer table
cursor.execute('''
CREATE TABLE Customer (
    SalesmanId INT,
    CustomerId INT,
    CustomerName VARCHAR(255),
    PurchaseAmount INT
)
''')

# Insert data into Customer
customer_data = [
    (101, 2345, 'Andrew', 550),
    (103, 1575, 'Lucky', 4500),
    (104, 2345, 'Andrew', 4000),
    (107, 3747, 'Remona', 2700),
    (110, 4004, 'Julia', 4545)
]
cursor.executemany('INSERT INTO Customer VALUES (?, ?, ?, ?)', customer_data)

# Create Orders table
cursor.execute('''
CREATE TABLE Orders (
    OrderId INT,
    CustomerId INT,
    SalesmanId INT,
    Orderdate DATE,
    Amount REAL
)
''')

# Insert data into Orders
orders_data = [
    (5001, 2345, 101, '2021-07-01', 550),
    (5003, 1234, 105, '2022-02-15', 1500)
]
cursor.executemany('INSERT INTO Orders VALUES (?, ?, ?, ?, ?)', orders_data)

# Task 1: Insert a new record in Orders table
cursor.execute('''
INSERT INTO Orders VALUES (5004, 1575, 103, '2023-01-10', 800)
''')

# Task 2: Add constraints
# Primary key for SalesmanId in Salesman (but SalesmanId is not unique, so perhaps it's meant to be unique)
# Actually, looking at data, SalesmanId seems unique, so we can add PRIMARY KEY
# But in SQLite, to add constraints after creation, we need to recreate table or use ALTER
# For simplicity, since it's initial, I'll recreate with constraints

# Drop and recreate Salesman with constraints
cursor.execute('DROP TABLE Salesman')
cursor.execute('''
CREATE TABLE Salesman (
    SalesmanId INT PRIMARY KEY,
    Name VARCHAR(255),
    Commission DECIMAL(10,2),
    City VARCHAR(255) DEFAULT 'Unknown',
    Age INT
)
''')
cursor.executemany('INSERT INTO Salesman VALUES (?, ?, ?, ?, ?)', salesman_data)

# Add Foreign key for SalesmanId in Customer
# In SQLite, foreign keys need to be enabled
cursor.execute('PRAGMA foreign_keys = ON')
cursor.execute('DROP TABLE Customer')
cursor.execute('''
CREATE TABLE Customer (
    SalesmanId INT,
    CustomerId INT,
    CustomerName VARCHAR(255) NOT NULL,
    PurchaseAmount INT,
    FOREIGN KEY (SalesmanId) REFERENCES Salesman(SalesmanId)
)
''')
cursor.executemany('INSERT INTO Customer VALUES (?, ?, ?, ?)', customer_data)

# Task 3: Fetch data where Customer’s name ending with ‘N’ and purchase amount > 500
cursor.execute('''
SELECT * FROM Customer WHERE CustomerName LIKE '%N' AND PurchaseAmount > 500
''')
task3_result = cursor.fetchall()
print("Task 3 Results:")
for row in task3_result:
    print(row)

# Task 4: Using SET operators, unique SalesmanId from two tables, and duplicates
# First result: unique SalesmanId from Salesman and Customer
cursor.execute('''
SELECT SalesmanId FROM Salesman
UNION
SELECT SalesmanId FROM Customer
''')
task4a_result = cursor.fetchall()
print("\nTask 4a (Unique SalesmanId):")
for row in task4a_result:
    print(row)

# Second result: SalesmanId with duplicates (using UNION ALL)
cursor.execute('''
SELECT SalesmanId FROM Salesman
UNION ALL
SELECT SalesmanId FROM Customer
''')
task4b_result = cursor.fetchall()
print("\nTask 4b (With duplicates):")
for row in task4b_result:
    print(row)

# Task 5: Display Orderdate, Salesman Name, Customer Name, Commission, City where Purchase Amount between 500 and 1500
cursor.execute('''
SELECT o.Orderdate, s.Name AS SalesmanName, c.CustomerName, s.Commission, s.City
FROM Orders o
JOIN Salesman s ON o.SalesmanId = s.SalesmanId
JOIN Customer c ON o.CustomerId = c.CustomerId
WHERE c.PurchaseAmount BETWEEN 500 AND 1500
''')
task5_result = cursor.fetchall()
print("\nTask 5 Results:")
for row in task5_result:
    print(row)

# Task 6: Using right join fetch all results from Salesman and Orders
# SQLite doesn't support RIGHT JOIN, use LEFT JOIN with swapped tables
cursor.execute('''
SELECT s.*, o.*
FROM Orders o
LEFT JOIN Salesman s ON o.SalesmanId = s.SalesmanId
''')
task6_result = cursor.fetchall()
print("\nTask 6 Results (Simulating RIGHT JOIN):")
for row in task6_result:
    print(row)

# Commit and close
conn.commit()
conn.close()
