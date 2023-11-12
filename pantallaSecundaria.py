import tkinter as tk


def pantallaSecundaria(sala:dict, pelicula:dict) -> None:
    
    window = tk.Tk(screenName='Pantalla Secundaria')
    
    window.title('PANTALLA SECUNDARIA')

    label_text = ' GRUPO 5 - Cines '
   
    texto1 = tk.Label(window, text = label_text, font = ("Trebuchet MS", 24, "bold"), bg = 'pink', fg = 'white')
    texto1.pack()
    
    botonPP = tk.Button(window, text=">> Volver a pantalla principal", command='Aca iria la funcion de pantalla principal')
    botonPP.configure(
        relief=tk.RAISED,
        bd=3,
        font=('Trebuchet MS', 7, 'bold'),
        foreground='white',
        background='#83BEAF',
        padx=10,
        pady=5,
    )
    botonPP.pack(pady=20)
    
    mostrarSala(sala, window)
    mostrarPelicula(pelicula, window)
    mostrarBotonReserva(sala, window)

    window.mainloop()
    
    
def mostrarSala(sala:dict, window:tk) -> None:
    
    cine_text = "- " + sala['location'] + " -"
    cine = tk.Label(window, text = cine_text, font = ('Trebuchet MS', 15), fg = 'pink')
    cine.pack(pady=10)
    
    asientos_text = "Asientos disponibles: " + str(sala['available_seats'])
    asientos = tk.Label(window, text = asientos_text, font = ('Trebuchet MS', 8, 'italic'), fg = 'black')
    asientos.pack()
    
    
def mostrarPelicula(pelicula:dict, window:tk) -> None:
    
    titulo_text = pelicula['name']
    titulo = tk.Label(window, text = titulo_text, font = ('Trebuchet MS', 10), fg = 'black')
    titulo.pack(pady=20)
    
    sinopsis_text = pelicula['synopsis']
    sinopsis = tk.Label(window, text = sinopsis_text, font = ('Trebuchet MS', 10, 'italic'), fg = 'black')
    sinopsis.pack()
    
    duracion_text = pelicula['duration']
    duracion = tk.Label(window, text = duracion_text, font = ('Trebuchet MS', 10), fg = 'black')
    duracion.pack()
    
    actores_text = pelicula['actors']
    actores = tk.Label(window, text = actores_text, font = ('Trebuchet MS', 10), fg = 'black')
    actores.pack()
    
    genero_text = pelicula['gender']
    genero = tk.Label(window, text = genero_text, font = ('Trebuchet MS', 10, 'bold'), fg = 'black')
    genero.pack()
    
    rating_text = pelicula['rating']
    rating = tk.Label(window, text = rating_text, font = ('Trebuchet MS', 10, 'bold'), fg = 'black')
    rating.pack()
    

def mostrarBotonReserva(sala:dict, window:tk) -> None:
    
    if sala['available_seats'] > 0:
    
        botonR = tk.Button(window, text="RESERVAR", command='Aca iria la funcion de pantalla de reserva')
        botonR.configure(
            relief=tk.RAISED,
            bd=3,
            font=('Trebuchet MS', 13, 'bold'),
            foreground='white',
            background='#ECCF94',
            padx=10,
            pady=15,
        )
        botonR.pack(pady=40)
        
    else:
        
        label_text = 'SALA LLENA - sin asientos disponibles.'
        label = tk.Label(window, text = label_text, font = ('Trebuchet MS', 13), fg = 'black', background='red', foreground='white')
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

pantallaSecundaria(sala, pelicula)
