import sqlite3 as sql
from typing import Any, Dict, List

##########################################################################

class DataBase:
    def __init__(self):
        self.dbLib = sql.connect("data.db")
        self.cur = self.dbLib.cursor()

    def close(self):
        self.cur.close()
        self.dbLib.close()

    # Initiation of database
    def create(self):
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS 
            Printed(
            student TEXT, 
            gradeLvl INTEGER, 
            section TEXT, 
            date TEXT,
            time TEXT 
            ) 
        """)
        self.dbLib.commit()

    def update(self, data: Dict[str, Any]):
        if not isinstance(data, dict):
            raise ValueError("Data must be a dictionary containing column names and values")

        cols = ", ".join(data.keys())
        vals = ", ".join(["?"] * len(data))
        
        check = self.cur.execute("SELECT COUNT(student) FROM Printed WHERE student=?", (data.get('student'),)).fetchone()[0]

        query = f"""
                INSERT INTO Printed ({cols})
                VALUES ({vals})
                """
        
        try:
            if not check:
                self.cur.execute(query, tuple(data.values()))
                self.dbLib.commit()
                print("Data successfully stored")
            else:
                # Updating Table Code here
                checkTwo = self.cur.execute("SELECT * FROM Printed WHERE student=?", (data['student'],)).fetchone()
                update = False

                for pos, (_, val) in enumerate(data.items()):
                    if checkTwo[pos] != val:
                        update = True
                        break

                if update:
                    valsPair = [f"{param}=?" for param in data.keys()]
                    updateQuery = f"""
                        UPDATE Printed
                        SET {", ".join(valsPair)} 
                        WHERE student=?
                    """
                    self.cur.execute(updateQuery, (*data.values(), data.get('student')))
                    self.dbLib.commit()
                    print("Successfully updated")
                else:
                    print("Data row exists, moving on")

        except sql.Error as err:
            print(f"Error occurred, refer back to source: {err}")

    def get(self, criteria: Dict[str, Any] = None) -> List[Any]:
        clause = []
        id = []

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
            print(f"Size array: {len(fetched)}")
            return fetched
        except sql.Error as err:
            print(f"Error occurred, please restart: {err}")
            return []

    def identities(self) -> int:
        self.cur.execute("SELECT COUNT(*) FROM Printed")
        return self.cur.fetchone()[0]

    def remove(self, id: Dict[str, Any]):
        query = f"""
            DELETE FROM Printed
            WHERE student=? 
        """
        try:
            self.cur.execute(query, (id['student'],))
            self.dbLib.commit()
            print("Successfully removed")
        except sql.Error as err:
            print(f"Cannot remove, invalid statements or syntax used: {err}")

##########################################################################

# TEST OF THE SQPY
if __name__ == "__main__":
    module = DataBase()
    module.create()

    module.update({"student": "Rafe", 'gradeLvl': 10, 'section': "Cepheus", 'date': '2/3/2023', 'time': '3:30am'})
    print(module.get({'student': 'Rafe', 'gradeLvl': 10}))
    print(module.identities())

    module.remove({'student': 'Rafe'})
    print(module.get({'student': 'Rafe'}))

    module.close()
