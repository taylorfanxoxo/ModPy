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
        self.cur.execute
        ("""

        CREATE TABLE IF NOT EXISTS 
            modules(
                name TEXT, 
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
        vals = ", ".join(["?"]*len(data))
        print(vals)

        query = f"""
                INSERT INTO modules ({cols})
                VALUES ({vals})
                """
        try: 
            self.cur.execute(query, list(data.values()) )
            self.dbLib.commit()
            print("data successfully stored")
        except sql.Error as err:
            print(f"error occured refer back to source, {err}")




    def get(self, criteria=None):
        clause = []
        id = []
        if criteria is None:
            query = "SELECT * FROM modules"

        else:
            for param, val in criteria.items():
                clause.append(f"{param} = ?")
                id.append(val)

            query = f"""
            SELECT * FROM modules
                WHERE {','.join(clause)} 
                    """
        try:
            self.cur.execute(query, id if id else [])
            fetched = self.cur.fetchall()
            print("Data fetching...")
            return fetched
        except:
            print('error occured please restart')



##########################################################################

if __name__ == "__main__":
    module = DataBase()
    module.create()

    module.insert(name = "MathA: Randomization", gradeLvl = 10, quarter = 2, number = 4, year = 2024)

    tThing = module.get(quarter="4")
    print(tThing)


    
