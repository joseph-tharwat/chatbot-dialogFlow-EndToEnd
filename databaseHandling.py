import mysql.connector

cnx = None
cursor = None

def databaseInit():
    global cnx
    global cursor

    cnx = mysql.connector.connect(
        host="localhost",
        port = 3306,
        user="root",
        database="food"
    )
    cursor = cnx.cursor()

def getItemPrice(item):
    global cursor

    # cursor.execute("SELECT * FROM itemprice WHERE item= %s", (item,)) #item must be tuple
    # cursor.execute("SELECT * FROM itemprice WHERE item= '{}'".format(item))   #format for substitution
    cursor.execute("SELECT * FROM itemprice WHERE item='" + item + "'")
    row = cursor.fetchall()
    itemPrice = row[0][1]

    return itemPrice


def getOrderPrice(id):
    global cursor

    cursor.execute("SELECT * FROM orders WHERE orderId='{}'".format(id))
    rows = cursor.fetchall()
    totalPrice = 0
    for row in rows:
        totalPrice = totalPrice + getItemPrice(row[1]) * row[2]

    return totalPrice

def getOrderItems(id):
    global cursor

    cursor.execute("SELECT * FROM orders WHERE orderId = '{}'".format(id))
    rows = cursor.fetchall()
    textItemsList = ""
    for row in rows:
        textItemsList = textItemsList + str(row[2]) +":"+ row[1] + ", "

    return textItemsList

def getAvailableId():
    cursor.execute("SELECT MAX(orderId) FROM orders")
    LastId = cursor.fetchall()[0][0]
    return LastId + 1


def storeNewOrder(sessionId, inProgressOrderDictionary):
    global cnx
    global cursor

    id = getAvailableId()
    inProgressOrderDictionary[sessionId]
    for item, num in inProgressOrderDictionary[sessionId].items():
        num = inProgressOrderDictionary[sessionId][item]
        cursor.execute("INSERT INTO `orders`(`orderId`, `item`, `number`) VALUES ('{}','{}','{}')".format(id, item, num))

    cnx.commit()

    return id

def closeDatabase():
    global cursor
    cursor.close()

