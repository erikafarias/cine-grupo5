import tkinter as tk
from PIL import ImageTk
import endpoints
from utils import decodificar_imagen_base64


def mostrar_pelicula(movie:dict, window:tk, movie_poster:str) -> None:
    
    poster = ImageTk.PhotoImage(decodificar_imagen_base64(movie_poster))
    poster_label = tk.Label(window, image=poster, bg='black')
    poster_label.pack(pady = 10)
    
    nombre_pelicula_texto = movie['name']
    nombre_pelicula = tk.Label(window, text = nombre_pelicula_texto, font = ('Calibri', 18, "bold"), bg='#2B2A33', fg = '#FFFFFF', anchor='center')
    nombre_pelicula.pack(pady = (30,10))
    
    sinopsis_texto = movie['synopsis']
    sinopsis = tk.Label(window, text = sinopsis_texto, font = ('Calibri', 10, 'italic'), bg='#2B2A33', fg = '#FFFFFF', wraplength = 600, justify= tk.CENTER)
    sinopsis.pack(pady = 5)
    
    duracion_texto = movie['duration']
    duracion = tk.Label(window, text = duracion_texto, font = ('Calibri', 10), bg='#2B2A33', fg = '#FFFFFF', anchor='center')
    duracion.pack(pady = 5)
    
    actores_texto = movie['actors']
    actores = tk.Label(window, text = actores_texto, font = ('Calibri', 10), bg='#2B2A33', fg = '#FFFFFF', anchor='center')
    actores.pack(pady = 5)
    
    genero_texto = movie['gender']
    genero = tk.Label(window, text = genero_texto, font = ('Calibri', 10, 'bold'), bg='#2B2A33', fg = '#FFFFFF', anchor='center')
    genero.pack(pady = 5)
    
    rating_texto = movie['rating']
    rating = tk.Label(window, text = rating_texto, font = ('Calibri', 10, 'bold'), bg='#2B2A33', fg = '#FFFFFF', anchor='center')
    rating.pack(pady = 5)


def mostrar_sala(cinema:dict, window:tk) -> None:
      
    asientos_texto = "Asientos disponibles:    " + str(cinema['available_seats'])
    asientos = tk.Label(window, text = asientos_texto, font = ('Calibri', 10, 'italic'), bg='#2B2A33', fg = '#FFFFFF', highlightthickness=1, padx=10)
    asientos.pack(pady = (60, 10))
    
    if cinema['available_seats'] > 0:

        boton_reserva = tk.Button(window, text="RESERVAR", command='pantalla_reserva()')
        boton_reserva.configure(
            relief=tk.RAISED,
            bd=3,
            font=('Calibri', 10, 'bold'),
            foreground='#FFFFFF',
            background='grey',
            padx=5,
            pady=5,
        )
        boton_reserva.pack(pady = 10)
        
    else:
        
        label_texto = 'SALA LLENA - sin asientos disponibles.'
        label = tk.Label(window, text = label_texto, font = ('Calibri', 13), bg='#2B2A33', fg = 'black', foreground='#FFFFFF')
        label.pack(pady = 10)


def pantalla_secundaria(window_principal:tk, ID_cinema:str, ID_pelicula:str) -> None:
    
    window_principal.withdraw() # Cierra la ventana anterior
    
    cinema:dict = endpoints.get_cinema_info_by_id(ID_cinema)
    movie:dict = endpoints.get_movie_by_id(ID_pelicula)
    movie_poster:str = endpoints.get_poster_by_id(movie['poster_id'])['poster_image']
    
    window = tk.Tk(screenName='Pantalla Secundaria')
    window.geometry("1280x720")
    window.configure(bg='#2B2A33')
    window.title('PANTALLA SECUNDARIA')
    
    # Titulo
    titulo_texto = cinema['location'].upper()
    titulo = tk.Label(window, text = titulo_texto, font = ("Calibri", 30, "bold", "underline"), bg = '#2B2A33', fg = 'grey', anchor='center')
    titulo.pack(pady = 15)
    
    # Boton pantalla principal
    boton_pantalla_principal = tk.Button(window, text=">> Volver a pantalla principal", command='pantalla_principal()')
    boton_pantalla_principal.configure(
        relief=tk.RAISED,
        bd=3,
        font=('Calibri', 8, 'bold'),
        foreground='#FFFFFF',
        background='black',
        padx=10,
        pady=5,
        anchor='center'
    )
    boton_pantalla_principal.pack(pady = 10)
    
    # Muestro la pelicula elegida
    mostrar_pelicula(movie, window, movie_poster)
    
    # Muestro sala con boton de reserva
    mostrar_sala(cinema, window)

    window.mainloop()


def main() -> None:
    
    # Diccionario que guarda toda la info correspondiente a la compra ha realizar. Se utiliza en todas las ventanas.
    compra: dict = {
        'ID_QR'             : '', # Este arrancatia vacio y se llena una vez realizada la compra y generado el QR
        'ID_pelicula'       : '2', # Pelicula elegida por el usuario en la pantalla principal
        'nombre_pelicula'   : '',
        'ID_cinema'         : '2', # Cine elegido por el usuario en la pantalla principal
        'cantidad_entradas' : 0,
        'precio_entrada'    : 0, # Este ya lo definimos aca hardcodeado
        'snacks'            : [ ['nombre snack', 'cantidad', 'precio unitario'] , ["nombre snack", 'cantidad', 'precio unitario'] ],
        'timestamp_compra'  : '' # Hora de la compra -> Cuando el usuario selecciona "comprar" en la pantalla checkout
    }

    pantalla_secundaria(window_principal, compra['ID_cinema'], compra['ID_pelicula'])

main()
