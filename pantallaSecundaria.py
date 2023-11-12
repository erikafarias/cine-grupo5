import tkinter as tk


def pantalla_secundaria(sala:dict, pelicula:dict) -> None:
    
    window = tk.Tk(screenName='Pantalla Secundaria')
    
    window.title('PANTALLA SECUNDARIA')

    titulo_texto = ' GRUPO 5 - Cines '
   
    titulo = tk.Label(window, text = titulo_texto, font = ("Trebuchet MS", 24, "bold"), bg = 'pink', fg = 'white')
    titulo.pack()
    
    boton_pantalla_principal = tk.Button(window, text=">> Volver a pantalla principal", command='Aca iria la funcion de pantalla principal')
    boton_pantalla_principal.configure(
        relief=tk.RAISED,
        bd=3,
        font=('Trebuchet MS', 7, 'bold'),
        foreground='white',
        background='#83BEAF',
        padx=10,
        pady=5,
    )
    boton_pantalla_principal.pack(pady=20)
    
    mostrar_sala(sala, window)
    mostrar_pelicula(pelicula, window)
    mostrar_boton_reserva(sala, window)

    window.mainloop()
    
    
def mostrar_sala(sala:dict, window:tk) -> None:
    
    cine_texto = "- " + sala['location'] + " -"
    cine = tk.Label(window, text = cine_texto, font = ('Trebuchet MS', 15), fg = 'pink')
    cine.pack(pady=10)
    
    asientos_texto = "Asientos disponibles: " + str(sala['available_seats'])
    asientos = tk.Label(window, text = asientos_texto, font = ('Trebuchet MS', 8, 'italic'), fg = 'black')
    asientos.pack()
    
    
def mostrar_pelicula(pelicula:dict, window:tk) -> None:
    
    nombre_pelicula_texto = pelicula['name']
    nombre_pelicula = tk.Label(window, text = nombre_pelicula_texto, font = ('Trebuchet MS', 10), fg = 'black')
    nombre_pelicula.pack(pady=20)
    
    sinopsis_texto = pelicula['synopsis']
    sinopsis = tk.Label(window, text = sinopsis_texto, font = ('Trebuchet MS', 10, 'italic'), fg = 'black')
    sinopsis.pack()
    
    duracion_texto = pelicula['duration']
    duracion = tk.Label(window, text = duracion_texto, font = ('Trebuchet MS', 10), fg = 'black')
    duracion.pack()
    
    actores_texto = pelicula['actors']
    actores = tk.Label(window, text = actores_texto, font = ('Trebuchet MS', 10), fg = 'black')
    actores.pack()
    
    genero_texto = pelicula['gender']
    genero = tk.Label(window, text = genero_texto, font = ('Trebuchet MS', 10, 'bold'), fg = 'black')
    genero.pack()
    
    rating_texto = pelicula['rating']
    rating = tk.Label(window, text = rating_texto, font = ('Trebuchet MS', 10, 'bold'), fg = 'black')
    rating.pack()
    

def mostrar_boton_reserva(sala:dict, window:tk) -> None:
    
    if sala['available_seats'] > 0:
    
        boton_reserva = tk.Button(window, text="RESERVAR", command='Aca iria la funcion de pantalla de reserva')
        boton_reserva.configure(
            relief=tk.RAISED,
            bd=3,
            font=('Trebuchet MS', 13, 'bold'),
            foreground='white',
            background='#ECCF94',
            padx=10,
            pady=15,
        )
        boton_reserva.pack(pady=40)
        
    else:
        
        label_texto = 'SALA LLENA - sin asientos disponibles.'
        label = tk.Label(window, text = label_texto, font = ('Trebuchet MS', 13), fg = 'black', background='red', foreground='white')
        label.pack(pady=40)

# la info de la sala se obtendria del endpoint GET /movies/{movie_id}/cinemas
sala:dict = {
    "cinema_id" : "1",
    "location" : "Caballito",
    "available_seats" : 10
}

# la info de pelicula se obtendria del endpoint GET /movies/{movie_id}
pelicula:dict = {
    "id" : "1",
    "poster_id" : "1",
    "release_date" : "",
    "name" : "BOOGEYMAN TU MIEDO ES REAL",
    "synopsis" : "Sadie Harper, una estudiante del colegio secundario y su hermana",
    "gender" : "Terror",
    "duration" : "98min",
    "actors" : "Chris Messina, David Dastmalchian, Sophie Thatcher",
    "directors" : "Rob Savage",
    "rating" : "+13"
}

pantalla_secundaria(sala, pelicula)
