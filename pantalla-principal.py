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


def find_movie_by_name(movie_name: str, cinema_id: str, movies_canvas: tk.Canvas):
    movies: list[dict] = find_movies_by_cinema(cinema_id)
    movies_found: list[dict] = []

    for movie in movies:
        if movie_name.upper() in movie['name'].upper():
            print(movie)
            movies_found.append(movie)

    if len(movies_found) == 0:
        movies_canvas.delete('all')
        label_no_disponibles = tk.Label(movies_canvas, text=f'No hay películas disponibles que coincidan con su búsqueda: {movie_name}', font='Calibri 18 bold', bg='#2B2A33', fg='#FFFFFF')
        label_no_disponibles.pack(fill='both', pady='10', padx='10', expand=True)
    else:
        show_movies(movies_found, movies_canvas)

    return movies_found


def show_movies(movies: list[dict], movies_canvas: tk.Canvas):
    number_of_movies: int = len(movies)
    number_of_rows: int = round(number_of_movies / 4) + 1
    NUMBER_OF_COLUMNS: int = 4

    movies_canvas.delete('all')

    movies_frame = tk.Frame(movies_canvas, bg='#2B2A33')
    movies_frame.pack(fill='both')
    movies_canvas.create_window((0, 0), window=movies_frame, anchor='nw')


    m: int = 0
    print(number_of_movies)

    for r in range(number_of_rows):
        for c in range(NUMBER_OF_COLUMNS):
            if m < number_of_movies:
                frame_movie = tk.Frame(movies_frame,bg='#2B2A33')
                frame_movie.grid(row=r, column=c, padx=10, pady=10)
                #poster_base64_movie = 'data:image/jpeg;base64,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'
                poster_base64_movie = find_poster(movies[m]['poster_id'])
                poster_movie = ImageTk.PhotoImage(decodificar_imagen_base64(poster_base64_movie))

                button_movie = tk.Button(frame_movie, image=poster_movie, bg='#2B2A33')
                button_movie.image = poster_movie # to prevent garbage collection
                button_movie.grid(row=0, column=0)

                label_movie = tk.Label(frame_movie, text=movies[m]['name'], font='Calibri 14', bg='#2B2A33', fg='#FFFFFF')
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
    select_cinema.config(font='Calibri 16 bold', bg=bg_color, fg=fg_color, width='50')
    select_cinema['menu'].config(font='Calibri 16', bg='#302F39', fg=fg_color)
    select_cinema.pack()
    frame_option_menu.pack(side='left')

    # search bar
    input_frame = tk.Frame(master=frame_cinemas_searchbar, bg=bg_color)
    movie_name = tk.StringVar()
    input_entry = tk.Entry(master=input_frame, textvariable=movie_name, font='Calibri 14', bg=bg_color, fg=fg_color)
    button = tk.Button(master=input_frame, text='Buscar', command=lambda: find_movie_by_name(movie_name.get(), cinema_id.get(), movies_canvas))
    button.configure(font='Calibri 14 bold', bg=bg_color, fg=fg_color, pady=0)
    input_entry.pack(side='left', padx='10')
    button.pack(side='right')
    input_frame.pack(side='right')

    frame_cinemas_searchbar.pack(pady=10)

    # posters
    movies_canvas = tk.Canvas(window, bg=bg_color)
    movies_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar = tk.Scrollbar(window, orient="vertical", bg=bg_color, command=movies_canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    movies_canvas.configure(yscrollcommand=scrollbar.set)

    show_movies(find_movies_by_cinema(cinema_id.get()), movies_canvas)

    window.mainloop()


pantalla_principal()
