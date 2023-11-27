import tkinter as tk
from PIL import ImageTk
import endpoints
from utils import decodificar_imagen_base64

WINDOW = tk.Tk()


def find_all_movies():
    movies: list[dict] = endpoints.get_movies()
    return movies


def find_movies_by_cinema(cinema_id: str) -> list[dict]:
    movies_by_cinema: list[dict] = endpoints.get_movies_by_cinema(cinema_id)
    all_movies: list[dict] = find_all_movies()
    movies: list[dict] = []
    for movie in all_movies:
        if movie['movie_id'] in movies_by_cinema[0]['has_movies']:
            movies.append(movie)

    return movies


def find_poster(poster_id: str) -> str:
    poster: dict = endpoints.get_poster_by_id(poster_id)
    return poster['poster_image']


def find_cinemas() -> list[dict]:
    cinemas: list[dict] = endpoints.get_cinemas()
    return cinemas


def list_cinemas_names(cinemas: list[dict]) -> list[str]:
    cinemas_names: list[str] = []
    for cinema in cinemas:
        cinemas_names.append(cinema['location'])

    return cinemas_names


def change_cinema(cinema_id: str, movies_container: tk.Canvas, window:tk, compra:dict):
    movies: list[dict] = find_movies_by_cinema(cinema_id)
    show_movies(movies, movies_container, window, compra)
    
    compra['ID_cinema'] = cinema_id


def find_cinema_id_by_name(cinemas: list[dict], cinema_name: str):
    for c in cinemas:
        if cinema_name == c['location']:
            return c['cinema_id']


def update_cinema_id(cinema_name: str, cinema_id: tk.StringVar, cinemas_list):
    cinema_id.set(find_cinema_id_by_name(cinemas_list, cinema_name))


def find_movie_by_name(movie_name: str, cinema_id: str, movies_canvas: tk.Canvas, entry: tk.Entry, window:tk, compra:dict):
    movies: list[dict] = find_movies_by_cinema(cinema_id)
    movies_found: list[dict] = []

    for movie in movies:
        if movie_name.upper() in movie['name'].upper():
            print(movie)
            movies_found.append(movie)

    if len(movies_found) == 0:
        movies_canvas.delete('all')
        label_no_disponibles = tk.Label(movies_canvas, text=f'No hay películas disponibles que coincidan con su '
                                                            f'búsqueda: {movie_name}', font='Calibri 18 bold',
                                        bg='#2B2A33', fg='#FFFFFF')
        label_no_disponibles.pack(fill='both', pady='10', padx='10', expand=True)
    else:
        show_movies(movies_found, movies_canvas, window, compra)

    entry.delete(0, tk.END)

    return movies_found


def show_movies(movies: list[dict], movies_canvas: tk.Canvas, window:tk, compra:dict):
    number_of_movies: int = len(movies)
    NUMBER_OF_COLUMNS: int = 4
    number_of_rows: int = round(number_of_movies / NUMBER_OF_COLUMNS) + 1

    movies_canvas.delete('all')

    movies_frame = tk.Frame(movies_canvas, bg='#2B2A33', highlightbackground='#2B2A33')
    movies_frame.pack(fill='both')
    movies_canvas.create_window((0, 0), window=movies_frame, anchor='nw')

    m: int = 0

    for r in range(number_of_rows):
        for c in range(NUMBER_OF_COLUMNS):
            if m < number_of_movies:
                
                frame_movie = tk.Frame(movies_frame, bg='#2B2A33')
                frame_movie.grid(row=r, column=c, padx=10, pady=10)
                poster_base64_movie = find_poster(movies[m]['poster_id'])
                poster_movie = ImageTk.PhotoImage(decodificar_imagen_base64(poster_base64_movie))
                
                button = tk.Button(frame_movie, image=poster_movie, bg='#2B2A33', command = lambda ID_movie = movies[m]['movie_id'] : pantalla_secundaria(window, compra, ID_movie))
                button.image = poster_movie  # to prevent garbage collection
                button.grid(row=0, column=0)
                
                label_movie = tk.Label(frame_movie, text=movies[m]['name'], font='Calibri 14', bg='#2B2A33',
                                       fg='#FFFFFF')
                label_movie.grid(row=1, column=0)

                m += 1

    movies_frame.update_idletasks()
    movies_canvas.update_idletasks()
    movies_canvas.config(scrollregion=movies_canvas.bbox('all'))


def pantalla_principal(compra:dict) -> None:
    bg_color = '#2B2A33'
    fg_color = '#FFFFFF'

    window = tk.Toplevel()
    window.title('Menu')
    window.geometry('1280x720')
    window.configure(bg='#2B2A33')

    # title
    title_label = tk.Label(master=window, text='Cartelera', font='Calibri 24 bold', bg=bg_color, fg=fg_color)
    title_label.pack()

    frame_cinemas_searchbar = tk.Frame(window, bg=bg_color)
    # select cinemas
    frame_option_menu = tk.Frame(frame_cinemas_searchbar, bg=bg_color)
    cinemas_list: list[dict] = find_cinemas()
    cinemas_names: list[str] = list_cinemas_names(cinemas_list)
    selected_cinema = tk.StringVar()
    cinema_id = tk.StringVar()
    selected_cinema.set(cinemas_names[0])
    cinema_id.set(find_cinema_id_by_name(cinemas_list, selected_cinema.get()))
    selected_cinema.trace_add('write', lambda *args: update_cinema_id(selected_cinema.get(), cinema_id, cinemas_list))
    select_cinema = tk.OptionMenu(frame_option_menu, selected_cinema, *cinemas_names,
                                  command=lambda event: change_cinema(cinema_id.get(), movies_canvas, window, compra))
    select_cinema.config(font='Calibri 16 bold', bg=bg_color, fg=fg_color, width='50', highlightbackground=bg_color)
    select_cinema['menu'].config(font='Calibri 16', bg='#302F39', fg=fg_color)
    select_cinema.pack()
    frame_option_menu.pack(side='left')

    # search bar
    input_frame = tk.Frame(master=frame_cinemas_searchbar, bg=bg_color, highlightbackground=bg_color)
    movie_name = tk.StringVar()
    input_entry = tk.Entry(master=input_frame, textvariable=movie_name, font='Calibri 14', bg=bg_color, fg=fg_color)
    button = tk.Button(master=input_frame, text='Buscar',
                       command=lambda: find_movie_by_name(movie_name.get(), cinema_id.get(), movies_canvas,
                                                          input_entry, window, compra))
    button.configure(font='Calibri 14 bold', bg=bg_color, fg=fg_color, pady=0, highlightbackground=bg_color)
    input_entry.pack(side='left', padx='10')
    button.pack(side='right')
    input_frame.pack(side='right')

    frame_cinemas_searchbar.pack(pady=10)
    
    # Guardo en el diccionario el cine elegido
    compra['ID_cinema'] = cinema_id.get()

    # posters
    movies_canvas = tk.Canvas(window, bg=bg_color, highlightbackground=bg_color)
    movies_canvas.pack(side='left', fill=tk.BOTH, expand=True)
    scrollbar = tk.Scrollbar(window, orient="vertical", bg=bg_color, command=movies_canvas.yview)
    scrollbar.pack(side='right', fill='y')
    movies_canvas.configure(yscrollcommand=scrollbar.set)

    show_movies(find_movies_by_cinema(cinema_id.get()), movies_canvas, window, compra)

    window.mainloop()


def mostrar_pelicula(movie:dict, window:tk) -> None:
    
    frame_movie = tk.Frame(window, bg='#2B2A33')
    frame_movie.pack(pady = 10)
    poster_base64_movie = find_poster(movie['poster_id'])
    poster = ImageTk.PhotoImage(decodificar_imagen_base64(poster_base64_movie))
    
    button_movie = tk.Button(frame_movie, image=poster, bg='#2B2A33', state='disabled')
    button_movie.image = poster  # to prevent garbage collection
    button_movie.pack()
    
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


def pantalla_secundaria(window_principal:tk, compra:dict, ID_movie:str) -> None:
        
    compra['ID_pelicula'] = ID_movie # Guardo el ID de la pelicula en el diccionario que viene del boton seleccionado
    
    window_principal.withdraw() # Cierra la ventana anterior
    
    cinema:dict = endpoints.get_cinema_info_by_id(compra['ID_cinema'])
    movie:dict = endpoints.get_movie_by_id(compra['ID_pelicula'])
    
    window = tk.Toplevel()
    window.geometry("1280x720")
    window.configure(bg='#2B2A33')
    window.title('PANTALLA SECUNDARIA')
    
    # Titulo
    titulo_texto = cinema['location'].upper()
    titulo = tk.Label(window, text = titulo_texto, font = ("Calibri", 30, "bold", "underline"), bg = '#2B2A33', fg = 'grey', anchor='center')
    titulo.pack(pady = 15)
    
    # Boton pantalla principal
    boton_pantalla_principal = tk.Button(window, text=">> Volver a pantalla principal", command= lambda : [window.withdraw(), pantalla_principal(compra)])
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
    mostrar_pelicula(movie, window)
    
    # Muestro sala con boton de reserva
    mostrar_sala(cinema, window)

    window.mainloop()


def pantalla_checkout(window_reserva:tk, compra:dict) -> None:
    
    window_reserva.withdraw() # Cierra la ventana anterior
    
    total:float = 0.0
    total_entradas:float = 0.0
    total_snacks:float = 0.0
    
    window = tk.Tk(screenName='Pantalla Checkout')
    window.geometry("1280x720")
    window.configure(bg= '#2B2A33')
    window.title('>>> CHECKOUT')
    
    # Titulo
    titulo_texto = ' 🛒 '
    titulo = tk.Label(window, text = titulo_texto, font = ("Calibri", 50, "bold"), bg= '#2B2A33', fg = 'white', anchor='center')
    titulo.pack(pady = 15)   
    titulo_texto2 = ' RESUMEN DE COMPRA '
    titulo2 = tk.Label(window, text = titulo_texto2, font = ("Calibri", 30, "bold"), bg= '#2B2A33', fg = 'white', anchor='center')
    titulo2.pack(pady = 15)
    
    canvas = tk.Canvas(window, bg= '#2B2A33', highlightbackground = '#2B2A33')
    canvas.pack(fill=tk.BOTH, padx=60, pady=30)
    
    # Entradas
    entradas_canvas = tk.Canvas(canvas, bg= '#2B2A33', highlightthickness = 3)
    entradas_canvas.pack(side=tk.LEFT, expand=1, fill=tk.BOTH, pady=15)
    
    titulo_entradas_texto = ' ENTRADAS '
    titulo_entradas = tk.Label(entradas_canvas, text = titulo_entradas_texto, font = ("Calibri", 20, "bold"), bg = 'white', fg = 'black', anchor='center')
    titulo_entradas.pack(pady = 20)   
    titulo_pelicula_texto = compra['nombre_pelicula']
    titulo_pelicula = tk.Label(entradas_canvas, text = titulo_pelicula_texto, font = ("Calibri", 15, "bold"), bg= '#2B2A33', fg = 'white', anchor='center')
    titulo_pelicula.pack(pady = 5)
    titulo_cantidad_entradas_texto = "- Entradas: " + str(compra['cantidad_entradas'])
    titulo_cantidad_entradas = tk.Label(entradas_canvas, text = titulo_cantidad_entradas_texto, font = ("Calibri", 10), bg= '#2B2A33', fg = 'white', anchor='center')
    titulo_cantidad_entradas.pack(pady = 5)   
    titulo_entradas_precio_texto = "- Precio Unitario: $" + str(compra['precio_entrada'])
    titulo_entradas_precio = tk.Label(entradas_canvas, text = titulo_entradas_precio_texto, font = ("Calibri", 10), bg= '#2B2A33', fg = 'white', anchor='center')
    titulo_entradas_precio.pack(pady = 5)   
    
    total_entradas = compra['cantidad_entradas']*compra['precio_entrada']
    
    titulo_entradas_total_texto = "TOTAL ENTRADAS: $" + str(total_entradas)
    titulo_entradas_total = tk.Label(entradas_canvas, text = titulo_entradas_total_texto, font = ("Calibri", 12, "bold"), bg = 'black', fg = 'white', anchor='center')
    titulo_entradas_total.pack(pady = (10, 25))  
    
    # Snacks
    snacks_canvas = tk.Canvas(canvas, bg= '#2B2A33', highlightthickness = 3)
    snacks_canvas.pack(side=tk.RIGHT, expand=1, fill=tk.BOTH, pady=15)
    
    titulo_snacks_texto = ' SNACKS '
    titulo_snacks = tk.Label(snacks_canvas, text = titulo_snacks_texto, font = ("Calibri", 20, "bold"), bg = 'white', fg = 'black', anchor='center')
    titulo_snacks.pack(pady = 20)
    
    for snack in compra['snacks']:
        titulo_snack_nombre_texto = "+ " + snack[0]
        titulo_snack_nombre = tk.Label(snacks_canvas, text = titulo_snack_nombre_texto, font = ("Calibri", 15, "bold"), bg= '#2B2A33', fg = 'white', anchor='center')
        titulo_snack_nombre.pack(pady = 10)
        titulo_cantidad_snack_texto = "Cantidad: " + str(snack[1])
        titulo_cantidad_snack = tk.Label(snacks_canvas, text = titulo_cantidad_snack_texto, font = ("Calibri", 10), bg= '#2B2A33', fg = 'white', anchor='center')
        titulo_cantidad_snack.pack(pady = 5)   
        titulo_snack_precio_texto = "Precio: $" + str(snack[1]*snack[2])
        titulo_snack_precio = tk.Label(snacks_canvas, text = titulo_snack_precio_texto, font = ("Calibri", 10), bg= '#2B2A33', fg = 'white', anchor='center')
        titulo_snack_precio.pack(pady = 5)
        
        total_snacks += snack[1]*snack[2]

    
    titulo_snacks_total_texto = "TOTAL SNACKS: $" + str(total_snacks)
    titulo_snacks_total = tk.Label(snacks_canvas, text = titulo_snacks_total_texto, font = ("Calibri", 12, "bold"), bg = 'black', fg = 'white', anchor='center')
    titulo_snacks_total.pack(pady = (10, 25))  
    
    # Total
    total = total_entradas + total_snacks
    
    titulo_total_texto = ' TOTAL: $' + str(total)
    titulo_total = tk.Label(window, text = titulo_total_texto, font = ("Calibri", 25, "bold"), bg = 'black', fg = 'white', anchor='center')
    titulo_total.pack(pady = 30)  
    
    boton_pagar = tk.Button(window, text="PAGAR", command='Aca iria la funcion para crear el QR')
    boton_pagar.configure(
        relief=tk.RAISED,
        bd=3,
        font=('Calibri', 15, 'bold'),
        foreground='white',
        background='grey',
        padx=20,
        pady=5,
    )
    boton_pagar.pack(pady = 15)
    

def main() -> None:
    
    # Diccionario que guarda toda la info correspondiente a la compra ha realizar. Se utiliza en todas las ventanas.
    compra: dict = {
        'ID_QR'             : '', # Este arrancatia vacio y se llena una vez realizada la compra y generado el QR
        'ID_pelicula'       : '', # Pelicula elegida por el usuario en la pantalla principal
        'ID_cinema'         : '', # Cine elegido por el usuario en la pantalla principal
        'cantidad_entradas' : 0,
        'precio_entrada'    : 0, # Este ya lo definimos aca hardcodeado
        'snacks'            : [ [] ],
        'timestamp_compra'  : '' # Hora de la compra -> Cuando el usuario selecciona "comprar" en la pantalla checkout
    }
    
    WINDOW.withdraw()

    pantalla_principal(compra)
    # pantalla_checkout(window_reserva, compra)

    WINDOW.mainloop()

main()
