import tkinter as tk
from PIL import ImageTk
import endpoints
from utils import decodificar_imagen_base64


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
            print(movie)

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


def change_cinema(cinema_id: str, movies_container: tk.Canvas):
    movies: list[dict] = find_movies_by_cinema(cinema_id)
    show_movies(movies, movies_container)


def find_cinema_id_by_name(cinemas: list[dict], cinema_name: str):
    for c in cinemas:
        if cinema_name == c['location']:
            return c['cinema_id']


def update_cinema_id(cinema_name: str, cinema_id: tk.StringVar, cinemas_list):
    cinema_id.set(find_cinema_id_by_name(cinemas_list, cinema_name))


def find_movie_by_name(movie_name: str, cinema_id: str):
    movies: list[dict] = find_movies_by_cinema(cinema_id)
    movies_found: list[dict] = []

    for movie in movies:
        if movie_name.upper() in movie['name'].upper():
            print(movie)
            movies_found.append(movie)

    if len(movies_found) == 0:
        print(f'No hay películas disponibles que coincidan con su búsqueda: {movie_name}')
    else:
        print(movies_found)

    return movies_found


def show_movies(movies: list[dict], movies_canvas: tk.Canvas):
    number_of_movies: int = len(movies)
    number_of_rows: int = round(number_of_movies / 2)
    NUMBER_OF_COLUMNS: int = 2

    scrollbar = tk.Scrollbar(movies_canvas, orient="vertical", command=movies_canvas.yview)
    scrollbar.grid(row=0, column=1, sticky="ns") #ns: north-south
    movies_canvas.configure(yscrollcommand=scrollbar.set)
    movies_frame = tk.Frame(movies_canvas)
    movies_frame.grid(row=0, column=0)
    movies_canvas.create_window((0, 0), window=movies_frame, anchor="nw")
    movies_canvas.config(scrollregion=movies_canvas.bbox("all"))

    m: int = 0
    print(number_of_movies)

    for r in range(number_of_rows):
        for c in range(NUMBER_OF_COLUMNS):
            if m < number_of_movies:
                frame_movie = tk.Frame(movies_canvas)
                frame_movie.grid(row=r, column=c, padx=10, pady=10)

                poster_base64_movie = find_poster(movies[m]['poster_id'])
                poster_movie = ImageTk.PhotoImage(decodificar_imagen_base64(poster_base64_movie))

                button_movie = tk.Button(frame_movie, image=poster_movie)
                button_movie.image = poster_movie # to prevent garbage collection
                button_movie.grid(row=0, column=0)

                label_movie = tk.Label(frame_movie, text=movies[m]['name'])
                label_movie.grid(row=1, column=0)

                print(m)
                m += 1
    print('FINNNNNNNN')
    movies_canvas.update_idletasks()


def pantalla_principal():
    window = tk.Tk()
    window.title('Menu')
    window.geometry('1280x720')
    window.configure(bg='#2B2A33')

    # title
    title_label = tk.Label(master=window, text='Cartelera', font='Calibri 24 bold')
    title_label.pack()

    # select cinemas
    cinemas_list: list[dict] = find_cinemas()
    cinemas_names: list[str] = list_cinemas_names(cinemas_list)
    selected_cinema = tk.StringVar()
    cinema_id = tk.StringVar()
    selected_cinema.set(cinemas_names[0])
    cinema_id.set(find_cinema_id_by_name(cinemas_list, selected_cinema.get()))
    selected_cinema.trace_add('write', lambda *args: update_cinema_id(selected_cinema.get(), cinema_id, cinemas_list))
    select_cinema = tk.OptionMenu(window, selected_cinema, *cinemas_names,
                                  command=lambda event: change_cinema(cinema_id.get(), movies_canvas))
    select_cinema.pack(padx=10, pady=10)

    # search bar
    input_frame = tk.Frame(master=window)
    movie_name = tk.StringVar()
    input_entry = tk.Entry(master=input_frame, textvariable=movie_name)
    button = tk.Button(master=input_frame, text='Buscar', command=lambda: find_movie_by_name(movie_name.get(), cinema_id.get()))
    input_entry.pack(side='left', padx=10)
    button.pack(side='right')
    input_frame.pack()

    # posters
    movies_canvas = tk.Canvas(window)
    movies_canvas.pack(side='left', fill='both', expand=True)
    show_movies(find_movies_by_cinema(cinema_id.get()), movies_canvas)

    window.mainloop()


pantalla_principal()
