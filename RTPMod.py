import sqlite3 as sql

##########################################################################

class DataBase:
    def __init__(self):
        self.dbLib = sql.connect("data.db")
        self.cur = self.dbLib.cursor()

    def __del__(self):
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


    def insert(self, data):

        if not isinstance(data, dict):
            raise ValueError("Data must be a dictionary containing column names and values")

        cols = ", ".join(data.keys())
        print(cols)
        vals = ", ".join(["?"] * len(data))

        query = f"""
                INSERT INTO Printed ({cols})
                VALUES ({vals})
                """

        try: 
            self.cur.execute(query, tuple(data.values()) )
            self.dbLib.commit()
            print("data successfully stored")

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
                clause.append(f"{param} = ?")
                id.append(val)

            query = f"""
            SELECT * FROM Printed 
                WHERE {','.join(clause)} 
                    """
        try:
            self.cur.execute(query, id)
            fetched = self.cur.fetchall()
            print("Data fetching...")
            print(f"Size array: ", len(fetched))
            return [things for things in fetched[0:len(fetched)-1]]
        except:
            print('error occured please restart')



##########################################################################

if __name__ == "__main__":
    module = DataBase()
    DataBase().create()

    module.insert({"titled" :"MathA: Randomization", "gradeLvl" : 10, "quarter" : 2, "number" : 4, "year" : 2024})
    module.insert({"titled" :"MathB: Log and Natural Log", "gradeLvl" : 10, "quarter" : 3, "number" : 1, "year" : 2022})
    module.insert({"titled": "ambot", "gradeLvl":10, 'quarter': 3, 'number': 1, 'year': 2022}) 


    tThing = module.get({"titled": "MathA: Randomization"})
    tThree = module.get({"gradeLvl": 10})

    print(tThing)
    print(tThree)

