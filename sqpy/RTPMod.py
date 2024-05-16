import sqlite3 as sql

##########################################################################

class DataBase:
    def __init__(self):
        self.dbLib = sql.connect("data.db")
        self.cur = self.dbLib.cursor()

    def close(self):
        self.cur.close()
        self.dbLib.close()

    #initiation of database
    def create(self):

        self.cur.execute("""

        CREATE TABLE IF NOT EXISTS 
            printed(
            titled TEXT, 
            gradeLvl INTEGER, 
            quarter INTEGER, 
            number INTEGER, 
            year INTEGER
            )

         """)
        
        self.dbLib.commit()


    def update(self, data):
        if not isinstance(data, dict):
            raise ValueError("Data must be a dictionary containing column names and values")

        cols = ", ".join(data.keys())
        vals = ", ".join(["?"] * len(data))
        
        check = self.cur.execute(f"SELECT COUNT(titled) FROM Printed WHERE titled='{data.get('titled')}' " ).fetchone()[0]

        query = f"""
                INSERT INTO Printed ({cols})
                VALUES ({vals})
                """
        
        try:
            if not check:
                self.cur.execute(query, tuple(data.values()) )
                self.dbLib.commit()
                print("data successfully stored")
            else:
                #Updating Table Code here
                checkTwo = self.cur.execute(f"""
                    SELECT * FROM Printed 
                    WHERE titled = '{data.get('titled')}' 
                """).fetchone()
                update = False

                for pos,(_, val) in enumerate(data.items()):
                    if checkTwo[pos] != val:
                        update = True
                        break

                if update:
                    valsPair = [f"{param}=?" for param in data.keys()]
                    print('phase2')
                    updateQuery = f"""
                        UPDATE Printed
                        SET {", ".join(valsPair)} 
                        WHERE titled = '{data.get('titled')}'
                    """
                    self.cur.execute(updateQuery, tuple(data.values()))
                    self.dbLib.commit()
                    print("successfully updated")

                else:
                    print("data row exists moving ~~ ~~ ~~ ~~")

        except sql.Error as err:
            print(f"\nerror occured refer back to source, {err}")




    def get(self, criteria):
        clause = []
        id = []

        if not isinstance(criteria, dict):
            raise ValueError("Data must be a dictionary containing column names and values")

        if criteria is None:
            query = "SELECT * FROM Printed"

        else:
            for param, val in criteria.items():
                clause.append(f"{param}=?")
                id.append(val)

            query = f"""
            SELECT * FROM Printed 
                WHERE ({' AND '.join(clause)}) 
                     """
        try:
            self.cur.execute(query, id)
            fetched = self.cur.fetchall()
            print("Data fetching...")
            print(f"Size array: ", len(fetched))
            return [things for things in fetched[0:len(fetched)]]
        except sql.Error as err:
            print(f'error occured please restart: {err}')
    
    identities = lambda self: self.cur.execute("SELECT COUNT(*) FROM Printed") 

    def identities(self):
        self.cur.execute("SELECT COUNT(*) FROM Printed")
        return self.cur.fetchall()[0][0]

    def remove(self, id):
        query = f"""
            SELECT * FROM Printed
                REMOVE * WHERE titled=?
        """
        try:
            self.cur.execute(query, id.get('titled'))
            self.dbLib.commit()
        except sql.Error as err:
            print(f"Cannot remove, invalid statements or syntax used: {err}")


##########################################################################

if __name__ == "__main__":
    module = DataBase()
    test = DataBase()
    test.create()
    module.create()

    test.update({"titled":'pizza', 'gradeLvl': 10, 'quarter': 9})
    module.update({"titled" :"MathA: Randomization", "gradeLvl" : 10, "quarter" : 2, "number" : 4, "year" : 2024})
    module.update({"titled" :"MathB: Log and Natural Log", "gradeLvl" : 10, "quarter" : 3, "number" : 1, "year" : 2022})
    module.update({"titled": "ambot", "gradeLvl":10, 'quarter': 3, 'number': 1, 'year': 2022}) 
    module.update({'titled' : "baynte", 'gradeLvl': 10, 'year':2022})
    module.update({'titled': 'test'})
    module.remove({"titled": 'test'})

    tThing = module.get({"year":2022,"gradeLvl":10})
    ttThing = test.get({'gradeLvl':10})


    print('modules ==>', tThing)
    print('food ==>', ttThing)
    print(module.identities())
    print(test.identities())

    module.close()
