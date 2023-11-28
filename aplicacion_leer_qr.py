import json
import tkinter
import cv2
from tkinter import messagebox


def camera() -> None:

    capture = cv2.VideoCapture(0)
    result, image = capture.read()
    if result:
        qr_detector = cv2.QRCodeDetector()
        data, bbox, rectified_image = qr_detector.detectAndDecode(image)

        if data:
            cv2.imshow('QR Code Reader', image)
            print(data)
            outfile = open('Ingresos.txt', 'a')
            outfile.write(f'\n{data}')
            outfile.close()
        else:
            messagebox.showinfo(message="No se pudo leer el QR", title="Error en lectura")

    else:
        messagebox.showinfo(message=f"No se pudo capturar la imagen", title="Error en captura")

    capture.release()
    cv2.destroyAllWindows()


def id_code(entry_code,string_info_show=None) -> None:
    code = str(entry_code.get())

    with open('IDs_QR.json', 'r') as file_:
        data = json.load(file_)

    string_info = ''

    if code in data:
        for element in data[code]:
            string_info += f'{element}; '

    if code not in data:
        messagebox.showinfo(message=f"No hay un ID asociado", title="Error en el ID")
 
    outfile = open('Ingresos.txt', 'a')
    outfile.write(string_info)
    outfile.close()

    string_info_show['text'] = string_info


def ventana() -> None:
    window = tkinter.Tk()
    window.geometry('800x600')
    window.title('Lector QR')
    window.resizable(False, False)
    window.configure(bg='#2b2a33')
    font_type = 'Calibri'

    # titulo2
    text1 = tkinter.Label(window, text='Lector QR', bg='#2b2a33',fg='#ffffff' , font=(font_type,20))
    text1.place(x=330, y=100)
    
    text2 = tkinter.Label(window, text='Ingresando el ID', bg='#2b2a33',fg='#ffffff' , font=(font_type,20))
    text2.place(x=100,y=200)

    text3 = tkinter.Label(
        window, 
        text='Escaneando el codigo QR', 
        bg='#2b2a33',
        fg='#ffffff', 
        font=(font_type,20))

    text3.place(x=470,y=200)


    # input id
    entry_code = tkinter.Entry(window, width=5 , font=(font_type,15))
    entry_code.place(x=140, y=280)
    entry_code.insert(0, '0000A')
    
    # info

    string_info_show = tkinter.Label(window, font=(font_type,15))
    string_info_show.place(x=170,y=450)


    # boton id
    button_id = tkinter.Button(window, text='Ingresar', command=lambda: id_code(entry_code,string_info_show))
    button_id.place(x=210,y=282)

    # boton camara

    button_camara = tkinter.Button(window, text="Escanear con la camara", command=lambda:camera())
    button_camara.place(x=530, y=282)


    window.mainloop()


def main() -> None:
    ventana()


main()