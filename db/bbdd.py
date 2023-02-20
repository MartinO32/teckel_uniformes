import sqlite3
from sqlite3 import Error, IntegrityError,ProgrammingError

class Bbdd():
    def __init__(self):
        self.create()

    def select(self,query=None, where=None,fetch=None):
        try:
            conexion=sqlite3.connect('db/teckelBD.db')
            cursor=conexion.cursor()
            cursor.execute(query,where)
            if fetch == 'fetchall':
                resultado=cursor.fetchall()
            else:
                resultado=cursor.fetchone()
            conexion.close()
            return resultado
        except ValueError:
            conexion=sqlite3.connect('db/teckelBD.db')
            cursor=conexion.cursor()
            cursor.execute(query)
            if fetch == 'fetchall':
                resultado=cursor.fetchall()
            else:
                resultado=cursor.fetchone()
            conexion.close()
            return resultado
    

    def insert_delete_update(self, query,where):
        conexion=sqlite3.connect('db/teckelBD.db')
        cursor=conexion.cursor()
        cursor.execute(query,where)
        conexion.commit()
        conexion.close()

    def create(self):
        proveedor = """ 
        CREATE TABLE IF NOT EXISTS proveedor (
        cuit INTEGER(11) PRIMARY KEY NOT NULL UNIQUE,
        descripcion TEXT NOT NULL UNIQUE,
        domicilio TEXT NOT NULL,
        telefono_1 TEXT NOT NULL,
        telefono_2 TEXT,
        telefono_3 TEXT,
        mail TEXT NOT NULL UNIQUE);
        """
        cliente= """ 
        CREATE TABLE IF NOT EXISTS cliente (
        cuit INTEGER(11) PRIMARY KEY NOT NULL UNIQUE,
        descripcion TEXT NOT NULL UNIQUE,
        domicilio TEXT NOT NULL,
        telefono_1 TEXT NOT NULL,
        telefono_2 TEXT,
        telefono_3 TEXT,
        mail TEXT NOT NULL UNIQUE);
        """
        conexion=sqlite3.connect('db/teckelBD.db')
        cursor=conexion.cursor()
        cursor.execute(proveedor)
        cursor.execute(cliente)
        

        


""" query='SELECT * FROM unidad_consumo WHERE descripcion LIKE ?'
buscar=['cm']
fetch='fetchone'

consulta=Bbdd()
print(consulta.select(query,buscar, fetch)) """

            