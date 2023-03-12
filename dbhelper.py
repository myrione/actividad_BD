import sqlite3
import os
from sqlite3 import Error
from config import cfg_item
from data_gathering import DataGathering

class DBHelper:
    def __init__(self, db=os.path.join(*cfg_item("database", "DB_file"))):
        self.dbname = db
               
        try:
            self.connection = sqlite3.connect(db)
            print('Conexión a la base de datos creada satisfactoriamente')
            self.connection.execute("PRAGMA foreign_keys = 1")
        except Error as e:
            print(f'Se ha producido el siguiente error: {e}')
        
        self.cursor = self.connection.cursor()
        
        
    def execute_query(self):
        
        self.connection.text_factory = str
        self.cursor.executescript('''CREATE TABLE IF NOT EXISTS DatosUsuario
        (
        Id INTEGER NOT NULL PRIMARY KEY UNIQUE, 
        NombreUsuario TEXT NOT NULL,
        Genero TEXT, 
        Edad TEXT,
        NivelConocimientos TEXT,
        Estudios TEXT,
        Ingresos TEXT
        Nacionalidad TEXT
        );'''
        )
        self.connection.commit()
        self.connection.close()   
    
    def check_user(self, update, user_data):
        self.connection.text_factory = str
        if len(self.cursor.execute('''SELECT Id FROM DatosUsuario WHERE Id = ?      ''', (update.message.from_user.id,)).fetchall())>0:
            c=self.cursor.execute('''SELECT NombreUsuario FROM DatosUsuario WHERE Id = ?''', str(update.message.from_user.username,)).fetchone()
            c=self.cursor('''SELECT Edad FROM DatosUsuario WHERE Id = ?''', (update.message.from_user.id,)).fetchone()
            user_data['Age']=c[0]
            c=self.cursor('''SELECT NivelConocimientos FROM DatosUsuario WHERE Id = ?''', (update.message.from_user.id,)).fetchone()
            user_data['Address']=c[0]
            c=self.cursor('''SELECT Estudios FROM DatosUsuario WHERE Id = ?''', (update.message.from_user.id,)).fetchone()
            user_data['Amount']=c[0]
            c=self.cursor('''SELECT Ingresos FROM DatosUsuario WHERE Id = ?''', (update.message.from_user.id,)).fetchone()
            user_data['Amount']=c[0]
            c=self.cursor('''SELECT Nacionalidad FROM DatosUsuario WHERE Id = ?''', (update.message.from_user.id,)).fetchone()
            user_data['Amount']=c[0]
            print('Past user')
        else:
            self.cursor.execute('''INSERT OR IGNORE INTO DatosUsuario (Id, NombreUsuario) VALUES (?, ?)''', \
            (update.message.from_user.id, update.message.from_user.first_name,))
            print('Nuevo usuario')
        
        self.connection.commit()
        self.connection.close()
    
    def update_user(self, category, text, update):
        self.connection.text_factory = str
        self.cursor.execute('''UPDATE OR IGNORE DatosUsuario SET {} = ? WHERE Id = ?'''.format(category), \
            (text, update.message.from_user.id,))
        self.connection.commit()
        self.connection.close()  