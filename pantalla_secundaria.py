import tkinter as tk
import endpoints


def pantalla_secundaria(cinema:dict, movie:dict) -> None:
    
    window = tk.Tk(screenName='Pantalla Secundaria')
    window.geometry("900x900")
    window.configure(bg='black')
    window.title('PANTALLA SECUNDARIA')
    
    # Titulo
    titulo_texto = ' GRUPO 5 - Cines '
    titulo = tk.Label(window, text = titulo_texto, font = ("Trebuchet MS", 24, "bold"), bg = 'red', fg = 'black', anchor='center')
    titulo.pack(pady = 15)
    
    # Boton pantalla principal
    boton_pantalla_principal = tk.Button(window, text=">> Volver a pantalla principal", command='Aca iria la funcion de pantalla principal')
    boton_pantalla_principal.configure(
        relief=tk.RAISED,
        bd=3,
        font=('Trebuchet MS', 7, 'bold'),
        foreground='white',
        background='black',
        padx=10,
        pady=5,
        anchor='center'
    )
    boton_pantalla_principal.pack(pady = 10)
    
    # Muestro la pelicula elegida
    mostrar_pelicula(movie, window)
    
    # Muestro sala con boton de reserva
    mostrar_sala(cinema, window)

    window.mainloop()


def mostrar_pelicula(pelicula:dict, window:tk) -> None:
    
    nombre_pelicula_texto = pelicula['name']
    nombre_pelicula = tk.Label(window, text = nombre_pelicula_texto, font = ('Trebuchet MS', 18, "bold"), bg = 'black', fg = 'orange', anchor='center')
    nombre_pelicula.pack(pady = (30,10))
    
    sinopsis_texto = pelicula['synopsis']
    sinopsis = tk.Label(window, text = sinopsis_texto, font = ('Trebuchet MS', 10, 'italic'), bg = 'black', fg = 'white', wraplength = 600, justify= tk.CENTER)
    sinopsis.pack(pady = 5)
    
    duracion_texto = pelicula['duration']
    duracion = tk.Label(window, text = duracion_texto, font = ('Trebuchet MS', 10), bg = 'black', fg = 'white', anchor='center')
    duracion.pack(pady = 5)
    
    actores_texto = pelicula['actors']
    actores = tk.Label(window, text = actores_texto, font = ('Trebuchet MS', 10), bg = 'black', fg = 'white', anchor='center')
    actores.pack(pady = 5)
    
    genero_texto = pelicula['gender']
    genero = tk.Label(window, text = genero_texto, font = ('Trebuchet MS', 10, 'bold'), bg = 'black', fg = 'white', anchor='center')
    genero.pack(pady = 5)
    
    rating_texto = pelicula['rating']
    rating = tk.Label(window, text = rating_texto, font = ('Trebuchet MS', 10, 'bold'), bg = 'black', fg = 'white', anchor='center')
    rating.pack(pady = 5)


def mostrar_sala(cinema:dict, window:tk) -> None:
    
    cine_texto = "- Sala " + cinema['location'] + " -"
    cine = tk.Label(window, text = cine_texto, font = ('Courier New', 15, 'bold'), bg = 'black', fg = 'red')
    cine.pack(pady = (70, 10))
    
    asientos_texto = "Asientos disponibles: " + str(cinema['available_seats'])
    asientos = tk.Label(window, text = asientos_texto, font = ('Trebuchet MS', 8, 'italic'), bg = 'black', fg = 'white', highlightthickness=1, padx=10)
    asientos.pack(pady = 10)
    
    if cinema['available_seats'] > 0:

        boton_reserva = tk.Button(window, text="RESERVAR", command='Aca iria la funcion de pantalla de reserva')
        boton_reserva.configure(
            relief=tk.RAISED,
            bd=3,
            font=('Trebuchet MS', 7, 'bold'),
            foreground='white',
            background='grey',
            padx=5,
            pady=5,
        )
        boton_reserva.pack(pady = 10)
        
    else:
        
        label_texto = 'SALA LLENA - sin asientos disponibles.'
        label = tk.Label(window, text = label_texto, font = ('Trebuchet MS', 13), bg = 'black', fg = 'black', foreground='white')
        label.pack(pady = 10)


movie:dict = endpoints.get_movie_by_id(2)
cinema:dict = endpoints.get_cinema_info_by_id(2)

pantalla_secundaria(cinema, movie)