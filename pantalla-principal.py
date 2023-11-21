import tkinter as tk
#from tkinter import ttk

def find_movie(movie_name: str):
    cinema = input_entry.get()
    return

def get_movies_by_cinema()

window = tk.Tk()
window.title = ('Menu')
window.geometry('800x600')

title_label = tk.Label(master=window, text='Cartelera', font='Calibri 24 bold')
title_label.pack()

input_frame = tk.Frame(master=window)
movie_name = tk.StringVar()
input_entry = tk.Entry(master=input_frame, textvariable=movie_name)
button = tk.Button(master=input_frame, text='Buscar', command=lambda: find_movie(movie_name))
input_entry.pack(side='left', padx=10)
button.pack(side='right')
input_frame.pack()



window.mainloop()




