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
            print(data)
            outfile = open('Ingresos.txt', 'a')
            outfile.write(f'\n{data}')
            outfile.close()
            messagebox.showinfo(message="QR escaneado correctamente. Disfrute su película!", title="QR válido")
        else:
            messagebox.showinfo(message="No se pudo leer el QR", title="Error en lectura")

    else:
        messagebox.showinfo(message=f"No se pudo capturar la imagen", title="Error en captura")

    capture.release()
    cv2.destroyAllWindows()


def id_code(entry_code) -> None:
    code = str(entry_code.get())

    with open('IDs_QR.json', 'r') as file_:
        data = json.load(file_)

    string_info = ''

    if code in data:
        for element in data[code]:
            string_info += f'{element}; '
        outfile = open('Ingresos.txt', 'a')
        outfile.write(f'\n{string_info}')
        outfile.close()
        messagebox.showinfo(message="Se validó correctamente el ID. Disfrute su película", title="ID válido")
    else:
        messagebox.showinfo(message=f"No hay un ID asociado", title="Error en el ID")


def ventana() -> None:
    bg_color = '#2b2a33'
    fg_color = '#ffffff'

    window = tkinter.Tk()
    window.geometry('800x600')
    window.title('Lector QR')
    window.resizable(False, False)
    window.configure(bg=bg_color)
    font_type = 'Calibri'

    title = tkinter.Label(window, text='Lector QR', bg='#2b2a33', fg='#ffffff', font=(font_type, 22, 'bold'))
    title.place(x=330, y=100)

    option_id = tkinter.Label(window, text='Ingresando el ID', bg='#2b2a33', fg='#ffffff', font=(font_type, 18, 'bold'))
    option_id.place(x=100, y=200)

    option_qr = tkinter.Label(window, text='Escaneando el codigo QR', bg=bg_color, fg=fg_color,
                              font=(font_type, 18, 'bold'))
    option_qr.place(x=470, y=200)

    entry_id = tkinter.Entry(window, width=5, font=(font_type, 14), bg=bg_color, fg=fg_color)
    entry_id.place(x=100, y=285)
    entry_id.insert(0, '0000A')

    button_id = tkinter.Button(window, text='Ingresar', command=lambda: id_code(entry_id))
    button_id.configure(font=(font_type, 14, 'bold'), bg=bg_color, fg=fg_color, pady=0, highlightbackground=bg_color)
    button_id.place(x=170, y=282)

    button_camera = tkinter.Button(window, text="Escanear con la camara", command=camera)
    button_camera.configure(font=(font_type, 14, 'bold'), bg=bg_color, fg=fg_color, pady=0,
                            highlightbackground=bg_color)
    button_camera.place(x=500, y=282)

    window.mainloop()


def main():
    ventana()


main()
