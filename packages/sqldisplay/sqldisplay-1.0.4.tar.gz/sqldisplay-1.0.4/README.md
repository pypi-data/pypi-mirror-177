# sqldisplay

## An extremely simple package to make displaying SQL queries much easier

### How does it work?
It simply takes cursor.description, as well as the query result and turns it into a readable format

### How do I use it?
Pretty simple, just install with pip(3):
`python3 -m pip install sqldisplay`

And then use it! (example)
```
import mysql.connector
from sqldisplay import sqldisplay

db = mysql.connector.connect(
    host="mysql-container",
    user="root",
    passwd="root",
    database="testdb"
)

cursor = db.cursor()

query = "SELECT * FROM Customers WHERE Country = 'USA';"
cursor.execute(query)
result = cursor.fetchall()
sqldisplay.format(cursor.description, result)
```
