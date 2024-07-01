import sqlite3
from dataclasses import dataclass

@dataclass
class Database_Admins:
    connect: sqlite3.Connection = None
    cursor: sqlite3.Cursor = None

    def __post_init__(self):
        self.connect = sqlite3.connect('admin.db')
        self.cursor = self.connect.cursor()

    def create_table(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS admin(
            id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            surname TEXT NOT NULL,
            contact TEXT NOT NULL,
            nikname TEXT NOT NULL)
        """)
        self.connect.commit()

    def add_admins(self, user_id, name, surname, contact, nikname):
        self.cursor.execute("INSERT INTO admin (user_id, name, surname, contact, nikname) VALUES (?, ?, ?, ?, ?)", (user_id, name, surname, contact, nikname))
        self.connect.commit()

    def select_admins(self):
        self.cursor.execute("SELECT * FROM admin") 
        return self.cursor.fetchall()
        
    def delete_one(self, id, value):
        self.cursor.execute(f"DELETE FROM admin WHERE {id}=?",(value,))
        self.connect.commit()

    def update_product(self,user_id,name,surname, contact,nikname):
        self.cursor.execute("UPDATE admin SET user_id = ?, name = ?, surname = ?, contact = ? WHERE id = ?",
                            (user_id,name,surname,contact,nikname)
                            ) 
        self.connect.commit()

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.connect:
            self.connect.close()
