import sqlite3

class ConexionDB:
    def __init__(self):
        
        #Se coloco doble \ ya que no queria tomar la ruta de la base da datos.
        self.base_datos='database/descargas.db' #Se indica la carpeta donde esta la base de datos y si no existe la crea.
        self.conexion= sqlite3.connect(self.base_datos)
        self.cursor = self.conexion.cursor()
        
        
    def cerrar_bd(self):
        self.conexion.commit()
        self.conexion.close()
        
        