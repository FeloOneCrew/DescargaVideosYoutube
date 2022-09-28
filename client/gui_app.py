from time import sleep
from tkinter import Label, PhotoImage, Variable, ttk
import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
import cv2
from turtle import bgcolor
from pytube import YouTube
import os
import imutils
from Model.descarga_dao import crear_tabla, borrar_tabla, Descarga, guardar, listar, eliminar
import numpy as np

def barra_menu(root):
    barra_menu= tk.Menu(root)
    root.config(menu= barra_menu, width= 300, height= 300)
    
    menu_inicio= tk.Menu(barra_menu, tearoff= 0)
    barra_menu.add_cascade(label= 'Inicio', menu= menu_inicio)
    
    menu_inicio.add_command(label='Crear registro en DB', command=crear_tabla )
    menu_inicio.add_command(label='Eliminar registro en DB', command= borrar_tabla)
    menu_inicio.add_command(label='Salir', command= root.destroy)

class Frame(tk.Frame):
    def __init__(self, root= None):
        super().__init__(root,width= 1700, height=1540)
        self.root= root
        self.pack()
        self.config(bg= "#212121")
        self.id_descarga = None
        self.cap = None
        self.campos_LinksDescarga()
        self.Desahabilitar_Campos()
        self.tabla_Descargas()

    def campos_LinksDescarga(self):
        #Label de cada campo.
        self.lbllink= tk.Label(self, text= 'Ingrese el link de Youtube: ')
        self.lbllink.config(font= ('Arial', 12, 'bold'), foreground= '#fff', background='#212121')
        self.lbllink.grid(row= 0, column= 0, padx= 10, pady= 10, columnspan= 4)
        
        self.lbllistbox= tk.Label(self, text='Elije el formato para la descarga: MP3 o MP4 ')
        self.lbllistbox.config(font= ('Arial', 12, 'bold'), foreground= '#fff', background= '#212121')
        self.lbllistbox.grid(row= 2, column= 0, padx= 10, pady= 10, columnspan= 4)
        
        #Label para los videos
        self.lblInfo1 = tk.Label(self, text="Video de entrada:")
        self.lblInfo1.config(font= ('Arial', 12, 'bold'), foreground= '#fff', background= '#212121')
        self.lblInfo1.grid(row=8, column=0)
        
        self.lblInfoVideoPath  = tk.Label(self, text="Aún no se ha seleccionado un video")
        self.lblInfoVideoPath.config(font= ('Arial', 12, 'bold'), foreground= '#fff', background= '#212121')
        self.lblInfoVideoPath .grid(row=8, column=1)
        
        self.lblvideo = tk.Label(self)
        self.lblvideo.config(foreground= '#fff', background= '#212121')
        self.lblvideo.grid(row= 9, column=0, columnspan= 4)
        
        #Entrys de cada campo
        self.mi_link = tk.StringVar()
        self.Entlink= tk.Entry(self, textvariable= self.mi_link)
        self.Entlink.config(width=50 , font= ('Arial', 12), background= '#666666')
        self.Entlink.grid(row= 1, column= 0, padx= 10, pady= 10, columnspan= 4)
        
        #Listbox
        self.listbox=tk.Listbox(self, exportselection= False)
        items = (
            ".MP3",
            ".MP4")
        self.listbox.insert(0, *items)
        self.listbox.config(width= 20, height= 4)
        self.listbox.select_set(0)
        self.listbox.grid(row= 3, column= 0, padx= 10, pady= 10, columnspan= 4)
        
        
        #Boton Descargar
        self.btndescargar= tk.Button(self, text= 'Descargar', command= self.datolink)
        self.btndescargar.config(width= 20, font= ('Arial', 12, 'bold'), fg= 'white', 
                             bg= '#FF0000', cursor= 'hand2', activebackground= '#FF7070') #Configuracion del boton
        self.btndescargar.grid(row= 4, column= 0, padx= 10, pady= 10)
        
        #Boton Nuevo
        self.btnNuevo= tk.Button(self, text= 'Nuevo', command= self.Desahabilitar_Campos)
        self.btnNuevo.config(width= 20, font= ('Arial', 12, 'bold'), fg= 'white', 
                             bg= '#56494C', cursor= 'hand2', activebackground= '#d1c1c5') #Configuracion del boton
        self.btnNuevo.grid(row= 4, column= 1, padx= 10, pady= 10)
        
        #Boton Salir 
        self.btnSalir= tk.Button(self, text= 'Salir', command= self.root.destroy)
        self.btnSalir.config(width= 20, font= ('Arial', 12, 'bold'), fg= 'white', 
                             bg= '#A3A3A3', cursor= 'hand2', activebackground= '#D6D6D6') #Configuracion del boton
        self.btnSalir.grid(row= 4, column= 2, padx= 10, pady= 10)
        
        #Boton Visualizar 
        self.btnVisualizar= tk.Button(self, text= 'Ver video', command= self.Visualizar_Video)
        self.btnVisualizar.config(width= 20, font= ('Arial', 12, 'bold'), fg= 'white', 
                             bg= '#FFFFFF', cursor= 'hand2', activebackground= '#999999', foreground='#111010') #Configuracion del boton
        self.btnVisualizar.grid(row= 7, column= 2, padx= 10, pady= 10)

    def habilitar_Campos(self):
        #habilitar campos para escribir
        self.Entlink.config(state= "normal")
        self.btnNuevo.config(state= "normal")
        
        #Deshabilitar
        self.btndescargar.config(state= "disabled")
        
    
    def Desahabilitar_Campos(self):
        #Deshabilitar campos para escribir
        self.id_link = None
        self.mi_link.set('') #Para que ponga el campo vacio
        self.btnNuevo.config(state= "disabled")
        self.btndescargar.config(state= "normal")
        self.btnVisualizar.config(state= "disabled")
   
    
    def datolink(self):
        self.habilitar_Campos()
        if self.mi_link.get() == "" :
            titulo = 'Verificar Link'
            mensaje = 'Por favor, ingresa un link de YouTube'
            messagebox.showerror(titulo, mensaje)
        
        else: 
            self.descarga()
        
    def itemSeleccionado(self):
        try:
            lista= self.listbox
            for self.item in lista.curselection():
                self.seleccion = tk.Label(self, text=lista.get(self.item))
                
        except:
            titulo = 'Verificar seleccion'
            mensaje = 'Por favor, elegir el formato de descarga'
            messagebox.showerror(titulo, mensaje)
                
    def descarga(self):
        self.habilitar_Campos()
        self.itemSeleccionado()
        selecion= self.item
        save = 'videos/'
        link = self.mi_link.get()
        ink= str(link)
        yt= YouTube(link)
        
        if selecion == 1:
            try:
                #VIDEO
                yt.streams.filter(progressive= True, file_extension= 'mp4').order_by('resolution').desc().first().download(save)
                titulo = 'Descarga video'
                mensaje = 'El video se descargó correctamente'
                messagebox.showinfo(titulo, mensaje)
                
            except:
                titulo = 'Verificar conección'
                mensaje = 'Connection Error'
                messagebox.showinfo(titulo, mensaje)
        else :
            try:
                # Extraer solo el audio
                video = yt.streams.filter(only_audio=True).first()
                destination = 'audios/' or '.' #str(input(">> ")) or '.'
                
                # descargar audio
                out_file = video.download(output_path=destination)
                
                # guardar audio
                base, ext = os.path.splitext(out_file)
                new_file = base + '.mp3'
                os.rename(out_file, new_file)
                
                # Resultado del proceso
                titulo = 'Descarga'
                self.nomCanc = yt.title
                self.autor= yt.author
                self.Views= yt.views
                impr= self.nomCanc + " has been successfully downloaded."
                mensaje = impr
                messagebox.showinfo(titulo, mensaje)
                
                self.guardar_datos()
        
            except:
                titulo = 'Verificar Descarga'
                mensaje = 'Connection Error'
                messagebox.showerror(titulo, mensaje)
    
    def guardar_datos(self):
        
        descarga = Descarga(self.nomCanc, self.autor, self.Views, self.mi_link.get())
        guardar(descarga)
        self.tabla_Descargas() #Se actualiza de manera automatica lo que este en BD
        #self.Desahabilitar_Campos()
    
    def tabla_Descargas(self):
        #Recuperar la tabla de peliculas
        self.lista_descargas = listar()
        self.lista_descargas.reverse()
         
        self.tabla = ttk.Treeview(self, columns= ('Descarga','Autor','Vistas','Link'))
        self.tabla.grid(row= 5, column=0, columnspan= 3, sticky= 'nsew')

        
        self.tabla.column('Descarga',anchor='center', width= 250)
        self.tabla.column('Autor',anchor='center', width= 100)
        self.tabla.column('Vistas',anchor='center', width= 70)
        self.tabla.column('Link',anchor='center')

        
        self.tabla.heading('#0', text='ID', anchor= 'center') # '#0' EL NUMERO DE LA COLUMNA CON EL ENCABEZADO
        self.tabla.heading('#1', text='DESCARGA', anchor= 'center')
        self.tabla.heading('#2', text='AUTOR', anchor= 'center')
        self.tabla.heading('#3', text='VISTAS', anchor= 'center')
        self.tabla.heading('#4', text='Link', anchor= 'center')
        
        #Scrollbar para la tabla si excede 10 registros
        self.scroll= ttk.Scrollbar(self, orient= 'vertical', command= self.tabla.yview)
        self.scroll.grid(row=5, column=3, sticky= 'nse')
        self.tabla.configure(yscrollcommand= self.scroll.set)
        
        self.scroll2= ttk.Scrollbar(self, orient= 'horizontal', command= self.tabla.xview)
        self.scroll2.grid(row= 5, column= 0, columnspan= 3, sticky= 'sew')
        self.tabla.configure(xscrollcommand= self.scroll2.set)
         
         
        #self.tabla.insert('',0, text= "1",values= ("ALDEANOS")) #Insertar datos de manera directa en la tabla.
        #Iterar la lista de peliculas

        for p in self.lista_descargas:

            self.tabla.insert('',0, text=p[0], 
                          values = (p[1], p[2], p[3], p[4])) #Insertando datos
    
        """
        #Boton Editar
        self.btnEditar= tk.Button(self, text= 'Editar')
        self.btnEditar.config(width= 20, font= ('Arial', 12, 'bold'), fg= 'white', 
                             bg= '#A6ACAF', cursor= 'hand2', activebackground= '#E5E7E9') #Configuracion del boton
        self.btnEditar.grid(row= 7, column= 0, padx= 10, pady= 10)
        """ 
        #Boton Eliminar
        self.btnEliminar= tk.Button(self, text= 'Eliminar Registro', command= self.eliminar_datos)
        self.btnEliminar.config(width= 20, font= ('Arial', 12, 'bold'), fg= 'white', 
                             bg= '#474747', cursor= 'hand2', activebackground= '#B8B8B8') #Configuracion del boton
        self.btnEliminar.grid(row= 7, column= 0, padx= 10, pady= 10)
        
    def eliminar_datos(self):
        try:
            self.id_descarga = self.tabla.item(self.tabla.selection())['text']
            eliminar( self.id_descarga)
            
            self.tabla_Descargas()
        except:
            titulo = 'Verificar Descarga'
            mensaje = 'No se ha seleccionado algun registro para eliminar'
            messagebox.showerror(titulo, mensaje)

    
    def Visualizar_Video(self):
        if self.cap is not None:
             self.lblVideo.image = ""
             self.cap.release()
            
        self.video_path = filedialog.askopenfilename(filetypes = [
            ("all video format", ".mp4"),
            ("all video format", ".avi")]) #Leer estos tipos de videos.
        if len(self.video_path) > 0:
            self.lblInfoVideoPath.configure(text=self.video_path)
            self.cap = cv2.VideoCapture(self.video_path)
            
            while self.cap.isOpened():
                ret, im= self.cap.read()
                if ret == False:
                    break
                
                #imag = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
                #self.lblvideo = cv2.imshow('imagen', imag)
                
                im = imutils.resize(im, cv2.COLOR_BGR2RGB)
                im = Image.fromarray(im)
                img = ImageTk.PhotoImage(image=im)
                self.lblVideo.configure(image=img)
                self.lblVideo.image = img
                
                if cv2.waitKey(1) == 27:
                    break 
                
                sleep(1/30)
        
        
    """def Visualizar_Video(self):

        if self.cap is not None:
             self.lblVideo.image = ""
             self.cap.release()
            
        self.video_path = filedialog.askopenfilename(filetypes = [
            ("all video format", ".mp4"),
            ("all video format", ".avi")]) #Leer estos tipos de videos.
        if len(self.video_path) > 0:
            self.lblInfoVideoPath.configure(text=self.video_path)
            self.cap = cv2.VideoCapture(self.video_path)
            self.visualizar()
        else:
            self.lblInfoVideoPath.configure(text="Aún no se ha seleccionado un video")
    """    
        
        
    """def visualizar(self):
        
        if self.cap is not None:
            ret, frame = self.cap.read()
            if ret == True:
                frame = imutils.resize(frame, width=320)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                im = Image.fromarray(frame)
                img = ImageTk.PhotoImage(image=im)
                self.lblVideo.configure(image=img)
                self.lblVideo.image = img
                self.lblVideo.after(10, self.visualizar)
            else:
                self.lblInfoVideoPath.configure(text="Aún no se ha seleccionado un video")
                self.lblVideo.image = ""
                self.cap.release()
"""    
        