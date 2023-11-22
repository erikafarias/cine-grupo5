import tkinter as tk
#from tkinter import ttk
import endpoints


def find_all_movies():
    movies: list[dict] = endpoints.get_movies()
    return movies


def find_movies_by_cinema(cinema_id: str) -> list[dict]:
    movies_by_cinema: list[dict] = endpoints.get_movies_by_cinema(cinema_id)

    all_movies: list[dict] = find_all_movies()
    movies: list[dict] = []
    for movie in all_movies:
        if movie['movie_id'] in movies_by_cinema[0]['has_movies']:
            print(movie)

    return movies_by_cinema


def find_posters(movies: list[dict]):
    posters: list[dict] = []

    for movie in movies:
        poster: dict = endpoints.get_poster_by_id(movie['poster_id'])
        posters.append(poster)

    return posters


def find_cinemas() -> list[dict]:
    cinemas: list[dict] = endpoints.get_cinemas()
    return cinemas


def list_cinemas_names() -> list[str]:
    cinemas: list[dict] = find_cinemas()
    cinemas_names: list[str] = []
    for cinema in cinemas:
        cinemas_names.append(cinema['location'])

    return cinemas_names


def change_cinema(cinema):
    cinemas_list: list[dict] = find_cinemas()
    for c in cinemas_list:
        if cinema == c['location']:
            find_movies_by_cinema(c['cinema_id'])


def find_movie_by_name(movie_name: str, cinema_id: str):
    movies: list[dict] = find_movies_by_cinema(cinema_id)
    movies_found: list[dict] = []

    for movie in movies:
        if movie_name in movie['name']:
            movies_found.append(movie)

    return movies_found


def show_movies():
    return


window = tk.Tk()
window.title = ('Menu')
window.geometry('800x600')

title_label = tk.Label(master=window, text='Cartelera', font='Calibri 24 bold')
title_label.pack()
cinemas: list[str] = list_cinemas_names()
selected_cinema = tk.StringVar()
selected_cinema.set(cinemas[0])
select_cinema = tk.OptionMenu(window, selected_cinema, *cinemas, command=lambda event, cinema=selected_cinema: change_cinema(cinema.get()))
select_cinema.pack(padx=10, pady=10)

input_frame = tk.Frame(master=window)
movie_name = tk.StringVar()
input_entry = tk.Entry(master=input_frame, textvariable=movie_name)
button = tk.Button(master=input_frame, text='Buscar', command=lambda: find_movie_by_name(movie_name, selected_cinema))
input_entry.pack(side='left', padx=10)
button.pack(side='right')
input_frame.pack()





window.mainloop()




