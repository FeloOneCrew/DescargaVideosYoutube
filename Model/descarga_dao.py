from email.message import Message
from .conexion_db import ConexionDB
from tkinter import messagebox

def crear_tabla():
    conexion= ConexionDB()
    
    sql= '''
    CREATE TABLE descargas(
        id_descarga INTEGER,
        nombre VARCHAR(300),
        autor VARCHAR(100),
        views INTEGER,
        link VARCHAR(300),
        PRIMARY KEY(id_descarga AUTOINCREMENT)
    )'''
    
    try:
        conexion.cursor.execute(sql)
        conexion.cerrar_bd()
        
        
    except:
        titulo= 'Crear Registro'
        mensaje= 'La tabla en la BD, ya se encuentra creada'
        messagebox.showwarning(titulo, mensaje)

def borrar_tabla():
    conexion= ConexionDB()
    
    sql = 'DROP TABLE descargas'
    
    try:
        conexion.cursor.execute(sql)
        conexion.cerrar_bd()
        
        titulo= 'Borrar Registro'
        mensaje= 'La  tabla en la BD, se borro con éxito'
        messagebox.showinfo(titulo, mensaje)
        
    except:
        titulo= 'Borrar Registro'
        mensaje= 'No existe tabla de datos para eliminar'
        messagebox.showerror(titulo, mensaje)
    
class Descarga:
    def __init__(self, nombre, autor, views, link):
        
        self.id_descarga = None
        self.nombre = nombre
        self.autor = autor
        self.views = views
        self.link = link

    
    def __str__(self):
        return f'Descarga[{self.nombre}, {self.autor}, {self.views}, {self.link}]'
    
def guardar(descarga):
    conexion= ConexionDB()
        
    sql= f"""INSERT INTO descargas (nombre, autor, views, link)
    VALUES('{descarga.nombre}', '{descarga.autor}', '{descarga.views}', '{descarga.link}')"""
        
    try:
        conexion.cursor.execute(sql)
        conexion.cerrar_bd()
            
        titulo= 'Ingreso de Registro'
        mensaje= 'El registro se realizó de manera éxitosa'
        messagebox.showinfo(titulo, mensaje)
            
        
    except:
        titulo= 'Error en Registro'
        mensaje= 'El registro no se realizó, ya que no existe tabla creada. Por favor crea primero la tabla'
        messagebox.showwarning(titulo, mensaje)
         
def listar():
    conexion = ConexionDB()
    
    lista_Peliculas = []
    sql = 'SELECT * FROM descargas'
    
    try:
        conexion.cursor.execute(sql)
        lista_Peliculas = conexion.cursor.fetchall()
        conexion.cerrar_bd()
    
    except:
        titulo= 'Conexión al Registro'
        mensaje= 'Crea la tabla en la base de Datos'
        messagebox.showwarning(titulo, mensaje)
    
    return lista_Peliculas

def editar(descarga, id_descarga):
    conexion= ConexionDB()
    
    sql = f""" UPDATE descargas
    SET nombre = '{descarga.nombre}'
    WHERE id_descarga = {id_descarga}"""
    
    try:
        conexion.cursor.execute(sql)
        conexion.cerrar_bd()
    
    except:
        titulo= 'Edición de datos'
        mensaje= 'No se pudo realizar la edicion del registro'
        messagebox.showwarning(titulo, mensaje)
        

def eliminar(id_descarga):
    conexion= ConexionDB()
    
    sql = f'DELETE FROM descargas WHERE id_descarga = {id_descarga}'
    
    try:
        conexion.cursor.execute(sql)
        conexion.cerrar_bd()
    
    except:
        titulo= 'Eliminar datos'
        mensaje= 'No se pudo eliminar el registro'
        messagebox.showwarning(titulo, mensaje)