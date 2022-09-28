from pytube import YouTube
import os

while True:

    save = 'videos/'
    x = """
    _________________________________________________
    Por favor ingresar como quiere descargar el video:
    _________________________________________________
     1- VIDEO(.MP4)
     2- AUDIO(.MP3)
     3-Salir  
     _________________________________________________
    """
    opcion= input(x)
    
    link = input('Ingrese el link del video:\n >>')
    ink= str(link)
    yt= YouTube(link)
    
    if opcion == "1":
        try:
            #VIDEO
            yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download(save)
            print("El video se descargó correctamente")
        except:
            print("Connection Error")
    elif opcion == "2":
        try:
            # url input from user
            #yt = YouTube(
            #   str(input('Ingrese el link del video: \n>>')))
            
            # extract only audio
            video = yt.streams.filter(only_audio=True).first()
            
            # check for destination to save file
            #print("Enter the destination (leave blank for current directory)")
            destination = 'audios/' or '.' #str(input(">> ")) or '.'
            
            # download the file
            out_file = video.download(output_path=destination)
            
            # save the file
            base, ext = os.path.splitext(out_file)
            new_file = base + "_1" + '.mp3'
            os.rename(out_file, new_file)
            
            # result of success
            print(yt.title + " ha sido descargado con éxito.")
            
        except:
            print("Connection Error")
    elif opcion == "3":
        print("CERRANDO JUEGO")
        break
    
    else:
        print("Opción incorrecta. ingresar una opcion correcta")