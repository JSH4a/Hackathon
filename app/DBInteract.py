import random

import mysql.connector
import requests


class dbInteract:

    def __init__(self):
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="password",
            database="dataset"
        )
        self.conn = self.db.cursor(buffered=True)
        self.conn.execute("SELECT max(id) FROM PRODUCTS")
        self.maxProductId = self.conn.fetchone()[0]

    def addProduct(self, name: str, emissions: float, manufacturer: str, tags: str):
        self.conn.execute("SELECT max(id) FROM PRODUCTS")
        id = self.conn.fetchone()[0] + 1
        sql = "INSERT INTO PRODUCTS (id, name, emissions, manufacturer, tags) VALUES (%s, %s, %s, %s, %s);"
        vals = (id, name, emissions, manufacturer, tags)
        self.conn.execute(sql, vals)
        self.db.commit()

    def addCompany(self, name: str, emissions: int, tags: str):
        self.conn.execute("SELECT max(id) FROM COMPANIES")
        id = self.conn.fetchone()[0] + 1
        sql = "INSERT INTO COMPANIES (id, name, emissions, tags) VALUES (%s, %s, %s, %s);"
        vals = (id, name, emissions, tags)
        self.conn.execute(sql, vals)
        self.db.commit()

    # doesn't work
    def getRandomProduct(self):
        self.conn.execute("SELECT max(id) from PRODUCTS")

        self.conn.execute("SELECT * FROM PRODUCTS WHERE id=" + str(random.randint(0, int(self.conn.fetchone()[0]) + 1)))

        return self.conn.fetchone()

    def getProductsWithRange(self, ranger: int, id=None):
        if ranger > self.maxProductId:
            raise Exception("Error, range too large")
        choice = id
        # chooses a random product
        if id is None:
            choice = random.randint(0, self.maxProductId)

        self.conn.execute("SELECT * FROM PRODUCTS WHERE id=" + str(choice))

        result1 = self.conn.fetchone()

        product1id = result1[0]
        product1 = result1[1]
        product1Emissions = result1[2]

        # gets results ordered by emissions
        self.conn.execute("SELECT * FROM PRODUCTS ORDER BY emissions")
        results = self.conn.fetchall()

        # gets num of results with emissions>product1
        self.conn.execute("SELECT COUNT(*) FROM PRODUCTS where emissions>" + str(product1Emissions))
        found = False
        # if the range up would be out of the dataset
        if ranger >= self.conn.fetchone()[0]:
            for i in range(1, len(results) + 1):
                if ranger == 0:
                    toss = random.randint(0, 2)
                    if toss == 1:
                        return (results[len(results) - i][0], results[len(results) - i][1],
                                results[len(results) - i][2]), (product1id,
                                                                product1, product1Emissions)
                    else:
                        return (product1id, product1, product1Emissions), (
                            results[len(results) - i][0], results[len(results) - i][1], results[len(results) - i][2])
                if found:
                    ranger -= 1
                if results[len(results) - i][0] == choice:
                    found = True
        else:
            for i in range(0, len(results)):
                if ranger == 0:
                    toss = random.randint(0, 2)
                    if toss == 1:
                        return (results[i][0], results[i][1], results[i][2]), (product1id,
                                                                               product1, product1Emissions)
                    else:
                        return (product1id, product1, product1Emissions), (results[i][0], results[i][1], results[i][2])
                if found:
                    ranger -= 1
                if results[i][0] == choice:
                    found = True

    def getNearbyProduct(self, id, ranger):
        self.getProductsWithRange(ranger, id=id)

    def getRandomFact(self, prevFactId=None):
        self.conn.execute("SELECT max(id) FROM FACTS")
        current = self.conn.fetchone()
        print(current[0])
        if prevFactId is None:
            choice = random.randint(0, current[0])
        else:
            choice = prevFactId
            while choice == prevFactId:
                choice = random.randint(0, current[0])
        stmt = "SELECT * FROM FACTS WHERE id=%s"
        vals = (choice,)
        self.conn.execute(stmt, vals)
        return self.conn.fetchone()

    # id of data, number who got it right, num who got it wrong
    def updateTimesSeen(self, id, correct: int, guesses: int):
        if id is not None and id <= self.maxProductId:
            self.conn.execute("SELECT timesSeen, timesCorrect FROM PRODUCTS WHERE id = " + str(id))
            result = self.conn.fetchone()
            stmt = "UPDATE PRODUCTS SET timesSeen=%s, timesCorrect=%s WHERE id=%s"
            vals = (result[0] + guesses, result[1] + correct, id)
            self.conn.execute(stmt, vals)
            self.db.commit()

    # returns a tuple (timesCorrect, timesSeen)
    def getPrevResults(self, id: int):
        stmt = "SELECT timesCorrect, timesSeen FROM PRODUCTS WHERE id=%s"
        vals = (id,)
        self.conn.execute(stmt, vals)
        return self.conn.fetchone()

    def addFact(self, id, fact):
        stmt = "INSERT INTO FACTS (id, fact) VALUES (%s,%s)"
        vals = (id, fact)
        self.conn.execute(stmt, vals)
        self.db.commit()

    # must call on close
    def close(self):
        self.conn.close()
        self.db.close()

    # how does loadig screen work - does number of guessed right update as the lobby guesses?


db = dbInteract()
"""
file = open("facts.txt", encoding="utf8", errors='ignore')
count=0
for line in file:
    db.addFact(count, line)
    count+=1

db.close()
"""
"""
file = open("carbonData (2).txt", encoding="utf8", errors='ignore')
count = 0
for line in file:
    count += 1
    if count >141:
        #print("Line{}: {}".format(count, line.strip()))
        currentLine = "{} {}".format(count, line.strip()).replace("Line", "").replace(str(count),"").replace(" - ", "±").replace("$", "").replace(",", "").replace("\ufeff","").replace("  ", "").replace(" ", "%20")
        currentLine = currentLine.split("±")
        if "." in currentLine[2]:
            currentLine[2] = currentLine[2].replace(".", "")
        else:
            currentLine[2] = currentLine[2]+"00"
        url = "https://api.ditchcarbon.com/v1.0/product?name="+currentLine[0]+"&manufacturer="+currentLine[1]+"&price_cents="+currentLine[2]+"&price_currency=GBP"
        headers = {
            "accept": "application/json",
            "authorization": "Bearer e112c9aa3edab54da198096201dab502"
        }
        response = requests.get(url, headers=headers)
        response = response.json()
        print(response)
        #response = (response.text).replace("{\"carbon_footprint\":", "").replace("{\"name\":", "").replace("{\"manufacturer\":", "")
        if(response is not None):
            db.addProduct(currentLine[0].replace("%20", " "), response["carbon_footprint"], response["manufacturer"], "")
"""
db.close()

"""
    conn.execute("CREATE TABLE COMPANIES ("
                   "id int(6),"
                   "name VARCHAR(20) NOT NULL,"
                   "emissions int(20) NOT NULL,"
                   "tags VARCHAR(30) NOT NULL,"
                   "timesSeen int(7) DEFAULT 0,"
                   "timesCorrect int(7) DEFAULT 0)")
    """
"""
    conn.execute("CREATE TABLE products ("
                   "id int(6),"
                   "name VARCHAR(10) NOT NULL,"
                   "emissions DOUBLE (9,8) NOT NULL,"
                   "tags VARCHAR(30) NOT NULL,"
                   "timesSeen int(7) DEFAULT 0,"
                   "timesCorrect int(7) DEFAULT 0"
                   ")")
    """
