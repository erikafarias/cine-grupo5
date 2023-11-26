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


def find_movie_by_name(movie_name: str, cinema_id: str, movies_canvas: tk.Canvas, entry: tk.Entry):
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
        show_movies(movies_found, movies_canvas)

    entry.delete(0, tk.END)

    return movies_found


def show_movies(movies: list[dict], movies_canvas: tk.Canvas):
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

                button_movie = tk.Button(frame_movie, image=poster_movie, bg='#2B2A33')
                button_movie.image = poster_movie  # to prevent garbage collection
                button_movie.grid(row=0, column=0)

                label_movie = tk.Label(frame_movie, text=movies[m]['name'], font='Calibri 14', bg='#2B2A33',
                                       fg='#FFFFFF')
                label_movie.grid(row=1, column=0)

                m += 1

    movies_frame.update_idletasks()
    movies_canvas.update_idletasks()
    movies_canvas.config(scrollregion=movies_canvas.bbox('all'))


def pantalla_principal():
    bg_color = '#2B2A33'
    fg_color = '#FFFFFF'

    window = tk.Tk()
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
                                  command=lambda event: change_cinema(cinema_id.get(), movies_canvas))
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
                                                          input_entry))
    button.configure(font='Calibri 14 bold', bg=bg_color, fg=fg_color, pady=0, highlightbackground=bg_color)
    input_entry.pack(side='left', padx='10')
    button.pack(side='right')
    input_frame.pack(side='right')

    frame_cinemas_searchbar.pack(pady=10)

    # posters
    movies_canvas = tk.Canvas(window, bg=bg_color, highlightbackground=bg_color)
    movies_canvas.pack(side='left', fill=tk.BOTH, expand=True)
    scrollbar = tk.Scrollbar(window, orient="vertical", bg=bg_color, command=movies_canvas.yview)
    scrollbar.pack(side='right', fill='y')
    movies_canvas.configure(yscrollcommand=scrollbar.set)

    show_movies(find_movies_by_cinema(cinema_id.get()), movies_canvas)

    window.mainloop()


pantalla_principal()
