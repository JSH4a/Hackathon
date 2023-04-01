import random

import mysql.connector


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

    def addProduct(self, name: str, emissions: float, tags: str):
        self.conn.execute("SELECT max(id) FROM PRODUCTS")
        id = self.conn.fetchone()[0] + 1
        sql = "INSERT INTO PRODUCTS (id, name, emissions, tags) VALUES (%s, %s, %s, %s);"
        vals = (id, name, emissions, tags)
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

    def getProductsWithRange(self, ranger:int):

        if ranger > self.maxProductId:
            raise Exception("Error, range too large")

        # chooses a random product
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





    # must call on close
    def close(self):
        self.conn.close()
        self.db.close()

    # how does loadig screen work - does number of guessed right update as the lobby guesses?


db = dbInteract()
print(db.getPrevResults(-1))
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
