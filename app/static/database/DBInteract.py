import random

import mysql.connector
import requests

from images import Fetcher

class dbInteract:

    def __init__(self):
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="dataset"
        )
        self.conn = self.db.cursor(buffered=True)
        self.conn.execute("SELECT max(id) FROM PRODUCTS")
        self.maxProductId = self.conn.fetchone()[0]

    def addProduct(self, name: str, emissions: float, manufacturer:str, tags: str):
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

    def getProductsWithRange(self, ranger:int, id=None):

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
                        return (results[len(results)-i][0], results[len(results) - i][1], results[len(results) - i][2]), (product1id,
                        product1, product1Emissions)
                    else:
                        return (product1id, product1, product1Emissions), (results[len(results)-i][0], results[len(results) - i][1], results[len(results) - i][2])
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

    def getRandomFact(self, prevFact=None):
        self.conn.execute("SELECT max(id) FROM FACTS")
        choice = random.randint(0, self.conn.fetchone()[0])
        stmt = "SELECT * FROM FACTS WHERE id=%s"
        vals = (choice,)
        self.conn.execute(stmt, vals)
        return self.conn.fetchone()[1]

    #id of data, number who got it right, num who got it wrong
    def updateTimesSeen(self, id, correct:int, guesses:int):
        if(id is not None and id<=self.maxProductId):
            self.conn.execute("SELECT timesSeen, timesCorrect FROM PRODUCTS WHERE id = "+str(id))
            result = self.conn.fetchone()
            stmt = "UPDATE PRODUCTS SET timesSeen=%s, timesCorrect=%s WHERE id=%s"
            vals = (result[0]+guesses,result[1]+correct, id)
            self.conn.execute(stmt, vals)
            self.db.commit()

    #returns a tuple (timesCorrect, timesSeen)
    def getPrevResults(self, id:int):
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

# return ((productID,))
def getQuestions(numQ):
    questions = []

    db = dbInteract()

    productTuple = db.getProductsWithRange(random.randint(1, 40))
    for i in range(numQ):
        higherMode = round(random.randint(0, 1))
        if higherMode:
            if productTuple[0][2] >  productTuple[1][2]:
                answer = 0
            else:
                answer = 1
        else:
            if productTuple[0][2] < productTuple[1][2]:
                answer = 0
            else:
                answer = 1

        image_url1, image_url2 = Fetcher.getImage(productTuple[0][1]), Fetcher.getImage(productTuple[1][1])
        
        questions.append((productTuple, (image_url1,image_url2), higherMode, answer))

        productTuple = db.getProductsWithRange(10, productTuple[0][0])
        
    db.close()

    return questions

print(getQuestions(10))