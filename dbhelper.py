import sqlite3
import os
from sqlite3 import Error
from config import cfg_item

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
        Conocimientos TEXT,
        Estudios TEXT,
        Ingresos TEXT
        );'''
        )
        self.connection.commit()
  
    
    def check_user(self, update, data):
        self.connection.text_factory = str
        if len(self.cursor.execute('''SELECT Id FROM DatosUsuario WHERE Id = ?      ''', (update.message.from_user.id,)).fetchall())>0:
            # c=self.cursor.execute('''SELECT NombreUsuario FROM DatosUsuario WHERE Id = ?''', str(update.message.from_user.username,)).fetchone()
            c=self.cursor.execute('''SELECT Genero FROM DatosUsuario WHERE Id = ?''', (update.message.from_user.id,)).fetchone()
            data['Genero']=c[0]
            c=self.cursor.execute('''SELECT Edad FROM DatosUsuario WHERE Id = ?''', (update.message.from_user.id,)).fetchone()
            data['Edad']=c[0]
            c=self.cursor.execute('''SELECT Conocimientos FROM DatosUsuario WHERE Id = ?''', (update.message.from_user.id,)).fetchone()
            data['Conocimientos']=c[0]
            c=self.cursor.execute('''SELECT Estudios FROM DatosUsuario WHERE Id = ?''', (update.message.from_user.id,)).fetchone()
            data['Estudios']=c[0]
            c=self.cursor.execute('''SELECT Ingresos FROM DatosUsuario WHERE Id = ?''', (update.message.from_user.id,)).fetchone()
            data['Ingresos']=c[0]
            print('Past user')
        else:
            self.cursor.execute('''INSERT OR IGNORE INTO DatosUsuario (Id, NombreUsuario) VALUES (?, ?)''', \
            (update.message.from_user.id, update.message.from_user.first_name,))
            print('Nuevo usuario')
        
        self.connection.commit()
       
    
    def update_user(self, category, text, user_id):
        self.connection.text_factory = str
        self.cursor.execute('''UPDATE OR IGNORE DatosUsuario SET {} = ? WHERE Id = ?'''.format(category), \
            (text, user_id,))
        self.connection.commit()
       