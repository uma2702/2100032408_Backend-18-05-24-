import mysql.connector

host = "localhost"
port = "3306"
uname = "root"
pwd = "Uma@2704"
db = "saferteck"

try:
    db_conn = mysql.connector.connect(host=host, port=port, user=uname, password=pwd, database=db)
    print("Connected to database successfully")
except Exception as e:
    print(e)

db_cursor = db_conn.cursor()

def createtable():
    try:
        #create table Customers
        customers = """ CREATE TABLE Customers ( CustomerID INT PRIMARY KEY, FirstName VARCHAR(50), LastName VARCHAR(50), Email VARCHAR(100),  DateOfBirth DATE  ) """
        db_cursor.execute(customers)
        print("Customers table created successfully")

        #create table Products
        products = """CREATE TABLE Products (ProductID INT PRIMARY KEY, ProductName VARCHAR(100),Price DECIMAL(10, 2)) """
        db_cursor.execute(products)
        print("Products table created successfully")

        #create table Orders
        orders = """ CREATE TABLE Orders ( OrderID INT PRIMARY KEY, CustomerID INT, OrderDate DATE,  FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID)) """
        db_cursor.execute(orders)
        print("Orders table created successfully")

        #create table OrderItems
        orderitems = """CREATE TABLE OrderItems (OrderItemID INT PRIMARY KEY,OrderID INT, ProductID INT, Quantity INT, FOREIGN KEY (OrderID) REFERENCES Orders(OrderID),FOREIGN KEY (ProductID) REFERENCES Products(ProductID) )"""
        db_cursor.execute(orderitems)
        print("OrderItems table created successfully")

    except Exception as e:
        print(e)



def insertrecord():
    try:
        # Insert records into the Customers table
        customers = "INSERT INTO Customers (CustomerID, FirstName, LastName, Email, DateOfBirth) VALUES (%s, %s, %s, %s, %s)"
        values_customers = [
            (1, "John", "Doe", "john.doe@example.com", "1985-01-15"),
            (2, "Jane", "Smith", "jane.smith@example.com", "1990-06-20")
        ]
        db_cursor.executemany(customers, values_customers)
        db_conn.commit()
        print(db_cursor.rowcount, "Customer record(s) inserted successfully")

        # Insert records into the Products table
        products = "INSERT INTO Products (ProductID, ProductName, Price) VALUES (%s, %s, %s)"
        values_products = [
            (1, "Laptop", 1000.00),
            (2, "Smartphone", 600.00),
            (3, "Headphones", 100.00)
        ]
        db_cursor.executemany(products, values_products)
        db_conn.commit()
        print(db_cursor.rowcount, "Product record(s) inserted successfully")

        # Insert records into the Orders table
        orders = "INSERT INTO Orders (OrderID, CustomerID, OrderDate) VALUES (%s, %s, %s)"
        values_orders = [
            (1, 1, "2023-01-10"),
            (2, 2, "2023-01-12")
        ]
        db_cursor.executemany(orders, values_orders)
        db_conn.commit()
        print(db_cursor.rowcount, "Order record(s) inserted successfully")

        # Insert records into the OrderItems table
        orderitems = "INSERT INTO OrderItems (OrderItemID, OrderID, ProductID, Quantity) VALUES (%s, %s, %s, %s)"
        values_order_items = [
            (1, 1, 1, 1),
            (2, 1, 3, 2),
            (3, 2, 2, 1),
            (4, 2, 3, 1)
        ]
        db_cursor.executemany(orderitems, values_order_items)
        db_conn.commit()
        print(db_cursor.rowcount, "OrderItem record(s) inserted successfully")

    except Exception as e:
        print(e)

def query1():
    try:
        sql = "SELECT * FROM Customers"
        db_cursor.execute(sql)
        result = db_cursor.fetchall()
        for row in result:
            print(row)
    except Exception as e:
        print(e)

def query2():
    try:
        sql = "SELECT * FROM Orders WHERE OrderDate BETWEEN '2023-01-01' AND '2023-01-31'"
        db_cursor.execute(sql)
        result = db_cursor.fetchall()
        for row in result:
            print(row)
    except Exception as e:
        print(e)

def query3():
    try:
        sql = """
        SELECT Orders.OrderID, Orders.OrderDate, Customers.FirstName, Customers.LastName, Customers.Email
        FROM Orders
        JOIN Customers ON Orders.CustomerID = Customers.CustomerID
        """
        db_cursor.execute(sql)
        result = db_cursor.fetchall()
        for row in result:
            print(row)
    except Exception as e:
        print(e)

def query4(order_id):
    try:
        sql = """
        SELECT Products.ProductID, Products.ProductName, Products.Price, OrderItems.Quantity
        FROM OrderItems
        JOIN Products ON OrderItems.ProductID = Products.ProductID
        WHERE OrderItems.OrderID = %s
        """
        db_cursor.execute(sql, (order_id,))
        result = db_cursor.fetchall()
        for row in result:
            print(row)
    except Exception as e:
        print(e)

def query5():
    try:
        sql = """
        SELECT Customers.CustomerID, Customers.FirstName, Customers.LastName, SUM(Products.Price * OrderItems.Quantity) AS TotalSpent
        FROM Orders
        JOIN OrderItems ON Orders.OrderID = OrderItems.OrderID
        JOIN Products ON OrderItems.ProductID = Products.ProductID
        JOIN Customers ON Orders.CustomerID = Customers.CustomerID
        GROUP BY Customers.CustomerID, Customers.FirstName, Customers.LastName
        """
        db_cursor.execute(sql)
        result = db_cursor.fetchall()
        for row in result:
            print(row)
    except Exception as e:
        print(e)

def query6():
    try:
        sql = """
        SELECT Products.ProductID, Products.ProductName, SUM(OrderItems.Quantity) AS TotalOrdered
        FROM OrderItems
        JOIN Products ON OrderItems.ProductID = Products.ProductID
        GROUP BY Products.ProductID, Products.ProductName
        ORDER BY TotalOrdered DESC
        LIMIT 1
        """
        db_cursor.execute(sql)
        result = db_cursor.fetchall()
        for row in result:
            print(row)
    except Exception as e:
        print(e)

def query7():
    try:
        sql = """
        SELECT DATE_FORMAT(OrderDate, '%Y-%m') AS OrderMonth, COUNT(*) AS TotalOrders, SUM(Products.Price * OrderItems.Quantity) AS TotalSales
        FROM Orders
        JOIN OrderItems ON Orders.OrderID = OrderItems.OrderID
        JOIN Products ON OrderItems.ProductID = Products.ProductID
        WHERE YEAR(OrderDate) = 2023
        GROUP BY OrderMonth
        ORDER BY OrderMonth
        """
        db_cursor.execute(sql)
        result = db_cursor.fetchall()
        for row in result:
            print(row)
    except Exception as e:
        print(e)

def query8():
    try:
        sql = """
        SELECT Customers.CustomerID, Customers.FirstName, Customers.LastName, SUM(Products.Price * OrderItems.Quantity) AS TotalSpent
        FROM Orders
        JOIN OrderItems ON Orders.OrderID = OrderItems.OrderID
        JOIN Products ON OrderItems.ProductID = Products.ProductID
        JOIN Customers ON Orders.CustomerID = Customers.CustomerID
        GROUP BY Customers.CustomerID, Customers.FirstName, Customers.LastName
        HAVING TotalSpent > 1000
        """
        db_cursor.execute(sql)
        result = db_cursor.fetchall()
        for row in result:
            print(row)
    except Exception as e:
        print(e)

#createtable()
#insertrecord()

print("The customers:")
query1()

print("\nThe Orders placed in January(2023):")
query2()

print("\nDetails of each order including customer name and email:")
query3()

print("\nProducts purchased in order with OrderID = 1:")
query4(1)

print("\nTotal amount spent by each customer:")
query5()

print("\nMost popular product is:")
query6()

print("\nTotal no. of orders and total sales amount for each month in 2023:")
query7()

print("\nCustomers who have spent more than $1000:")
query8()