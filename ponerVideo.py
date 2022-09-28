from tkinter import *
from tkinter import filedialog
from PIL import Image
from PIL import ImageTk
import cv2
import imutils


def elegir_visualizar_video():
    global cap
    if cap is not None:
        lblVideo.image = ""
        cap.release()
        cap = None
    video_path = filedialog.askopenfilename(filetypes = [
        ("all video format", ".mp4"),
        ("all video format", ".avi")])
    if len(video_path) > 0:
        lblInfoVideoPath.configure(text=video_path)
        cap = cv2.VideoCapture(video_path)
        visualizar()
    else:
        lblInfoVideoPath.configure(text="Aún no se ha seleccionado un video")
        

def visualizar():
    global cap
    if cap is not None:
        ret, frame = cap.read()
        if ret == True:
            frame = imutils.resize(frame, width=640)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            im = Image.fromarray(frame)
            img = ImageTk.PhotoImage(image=im)
            lblVideo.configure(image=img)
            lblVideo.image = img
            lblVideo.after(10, visualizar)
        else:
            lblInfoVideoPath.configure(text="Aún no se ha seleccionado un video")
            lblVideo.image = ""
            cap.release()

cap = None
root = Tk()
btnVisualizar = Button(root, text="Elegir y visualizar video", command=elegir_visualizar_video)
btnVisualizar.grid(column=0, row=0, padx=5, pady=5, columnspan=2)
lblInfo1 = Label(root, text="Video de entrada:")
lblInfo1.grid(column=0, row=1)
lblInfoVideoPath = Label(root, text="Aún no se ha seleccionado un video")
lblInfoVideoPath.grid(column=1, row=1)
lblVideo = Label(root)
lblVideo.grid(column=0, row=2, columnspan=2)
root.mainloop()