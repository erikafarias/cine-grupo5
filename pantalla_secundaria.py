import tkinter as tk
from PIL import ImageTk
import endpoints
from utils import decodificar_imagen_base64


def mostrar_pelicula(pelicula:dict, window:tk, movie_poster:str) -> None:
    
    poster = ImageTk.PhotoImage(decodificar_imagen_base64(movie_poster))
    poster_label = tk.Label(window, image=poster, bg='black')
    poster_label.pack(pady = 10)
    
    nombre_pelicula_texto = pelicula['name']
    nombre_pelicula = tk.Label(window, text = nombre_pelicula_texto, font = ('Calibri', 18, "bold"), bg='#2B2A33', fg = '#FFFFFF', anchor='center')
    nombre_pelicula.pack(pady = (30,10))
    
    sinopsis_texto = pelicula['synopsis']
    sinopsis = tk.Label(window, text = sinopsis_texto, font = ('Calibri', 10, 'italic'), bg='#2B2A33', fg = '#FFFFFF', wraplength = 600, justify= tk.CENTER)
    sinopsis.pack(pady = 5)
    
    duracion_texto = pelicula['duration']
    duracion = tk.Label(window, text = duracion_texto, font = ('Calibri', 10), bg='#2B2A33', fg = '#FFFFFF', anchor='center')
    duracion.pack(pady = 5)
    
    actores_texto = pelicula['actors']
    actores = tk.Label(window, text = actores_texto, font = ('Calibri', 10), bg='#2B2A33', fg = '#FFFFFF', anchor='center')
    actores.pack(pady = 5)
    
    genero_texto = pelicula['gender']
    genero = tk.Label(window, text = genero_texto, font = ('Calibri', 10, 'bold'), bg='#2B2A33', fg = '#FFFFFF', anchor='center')
    genero.pack(pady = 5)
    
    rating_texto = pelicula['rating']
    rating = tk.Label(window, text = rating_texto, font = ('Calibri', 10, 'bold'), bg='#2B2A33', fg = '#FFFFFF', anchor='center')
    rating.pack(pady = 5)


def mostrar_sala(cinema:dict, window:tk) -> None:
      
    asientos_texto = "Asientos disponibles:    " + str(cinema['available_seats'])
    asientos = tk.Label(window, text = asientos_texto, font = ('Calibri', 10, 'italic'), bg='#2B2A33', fg = '#FFFFFF', highlightthickness=1, padx=10)
    asientos.pack(pady = (60, 10))
    
    if cinema['available_seats'] > 0:

        boton_reserva = tk.Button(window, text="RESERVAR", command='Aca iria la funcion de pantalla de reserva')
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


def pantalla_secundaria(cinema:dict, movie:dict, movie_poster:str) -> None:
    
    window = tk.Tk(screenName='Pantalla Secundaria')
    window.geometry("1280x720")
    window.configure(bg='#2B2A33')
    window.title('PANTALLA SECUNDARIA')
    
    # Titulo
    titulo_texto = cinema['location'].upper()
    titulo = tk.Label(window, text = titulo_texto, font = ("Calibri", 30, "bold", "underline"), bg = '#2B2A33', fg = 'grey', anchor='center')
    titulo.pack(pady = 15)
    
    # Boton pantalla principal
    boton_pantalla_principal = tk.Button(window, text=">> Volver a pantalla principal", command='Aca iria la funcion de pantalla principal')
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


movie:dict = endpoints.get_movie_by_id('3')
movie_poster:str = endpoints.get_movie_poster('3')
cinema:dict = endpoints.get_cinema_info_by_id('3')

pantalla_secundaria(cinema, movie, movie_poster)
