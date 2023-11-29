import datetime
import json
import locale
import random
import string
import tkinter as tk
from tkinter import ttk, messagebox

import qrcode  # pip install qrcode
from PIL import ImageTk, Image

import endpoints
from utils import decodificar_imagen_base64

WINDOW = tk.Tk()


def find_movies_by_cinema(cinema_id: str) -> list[dict]:
    movies_by_cinema: list[dict] = endpoints.get_movies_by_cinema(cinema_id)
    all_movies: list[dict] = endpoints.get_movies()
    movies: list[dict] = []
    for movie in all_movies:
        if movie['movie_id'] in movies_by_cinema[0]['has_movies']:
            movies.append(movie)

    return movies


def list_cinemas_names(cinemas: list[dict]) -> list[str]:
    cinemas_names: list[str] = []
    for cinema in cinemas:
        cinemas_names.append(cinema['location'])

    return cinemas_names


def change_cinema(cinema_id: str, movies_container: tk.Canvas, window: tk, sale: dict) -> None:
    movies: list[dict] = find_movies_by_cinema(cinema_id)
    show_movies(movies, movies_container, window, sale)

    sale['ID_cinema'] = cinema_id
    sale['ubicacion_totem'] = (endpoints.get_cinema_info_by_id(cinema_id))['location']


def find_cinema_id_by_name(cinemas: list[dict], cinema_name: str) -> str:
    for c in cinemas:
        if cinema_name == c['location']:
            return c['cinema_id']


def update_cinema_id(cinema_name: str, cinema_id: tk.StringVar, cinemas_list: list) -> None:
    cinema_id.set(find_cinema_id_by_name(cinemas_list, cinema_name))


def find_movie_by_name(movie_name: str, cinema_id: str, movies_canvas: tk.Canvas, entry: tk.Entry, window: tk,
                       sale: dict) -> list[dict]:
    movies: list[dict] = find_movies_by_cinema(cinema_id)
    movies_found: list[dict] = []

    for movie in movies:
        if movie_name.upper() in movie['name'].upper():
            movies_found.append(movie)

    if len(movies_found) == 0:
        movies_canvas.delete('all')
        label_no_disponibles = tk.Label(movies_canvas, text=f'No hay películas disponibles que coincidan con su '
                                                            f'búsqueda: {movie_name}', font='Calibri 18 bold',
                                        bg='#2B2A33', fg='#FFFFFF')
        label_no_disponibles.pack(fill='both', pady='10', padx='10', expand=True)
    else:
        show_movies(movies_found, movies_canvas, window, sale)

    entry.delete(0, tk.END)

    return movies_found


def show_movies(movies: list[dict], movies_canvas: tk.Canvas, window: tk, sale: dict) -> None:
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
                poster_base64_movie = endpoints.get_poster_by_id(movies[m]['poster_id'])
                poster_movie = ImageTk.PhotoImage(decodificar_imagen_base64(poster_base64_movie))

                button = tk.Button(frame_movie, image=poster_movie, bg='#2B2A33',
                                   command=lambda ID_movie=movies[m]['movie_id']: secondary_window(window, sale,
                                                                                                   ID_movie))
                button.image = poster_movie  # to prevent garbage collection
                button.grid(row=0, column=0)

                label_movie = tk.Label(frame_movie, text=movies[m]['name'], font='Calibri 14', bg='#2B2A33',
                                       fg='#FFFFFF')
                label_movie.grid(row=1, column=0)

                m += 1

    movies_frame.update_idletasks()
    movies_canvas.update_idletasks()
    movies_canvas.config(scrollregion=movies_canvas.bbox('all'))


def principal_window(sale: dict) -> None:
    bg_color = '#2B2A33'
    fg_color = '#FFFFFF'

    window = tk.Toplevel()
    window.title('Menu')
    window.geometry('1280x720')
    window.configure(bg='#2B2A33')

    # title
    title_label = tk.Label(master=window, text='🎬 CARTELERA', font='Calibri 24 bold', bg=bg_color, fg=fg_color)
    title_label.pack(pady=10)

    frame_cinemas_searchbar = tk.Frame(window, bg=bg_color)
    # select cinemas
    frame_option_menu = tk.Frame(frame_cinemas_searchbar, bg=bg_color)
    cinemas_list: list[dict] = endpoints.get_cinemas()
    cinemas_names: list[str] = list_cinemas_names(cinemas_list)
    selected_cinema = tk.StringVar()
    cinema_id = tk.StringVar()
    selected_cinema.set(cinemas_names[0])
    cinema_id.set(find_cinema_id_by_name(cinemas_list, selected_cinema.get()))
    selected_cinema.trace_add('write', lambda *args: update_cinema_id(selected_cinema.get(), cinema_id, cinemas_list))
    select_cinema = tk.OptionMenu(frame_option_menu, selected_cinema, *cinemas_names,
                                  command=lambda event: change_cinema(cinema_id.get(), movies_canvas, window, sale))
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
                                                          input_entry, window, sale))
    button.configure(font='Calibri 14 bold', bg=bg_color, fg=fg_color, pady=0, highlightbackground=bg_color)
    input_entry.pack(side='left', padx='10')
    button.pack(side='right')
    input_frame.pack(side='right')

    frame_cinemas_searchbar.pack(pady=10)

    # Guardo en el diccionario el cine elegido
    sale['ID_cinema'] = cinema_id.get()
    sale['ubicacion_totem'] = selected_cinema.get()

    # posters
    movies_canvas = tk.Canvas(window, bg=bg_color, highlightbackground=bg_color)
    movies_canvas.pack(side='left', fill=tk.BOTH, expand=True)
    scrollbar = tk.Scrollbar(window, orient="vertical", bg=bg_color, command=movies_canvas.yview)
    scrollbar.pack(side='right', fill='y')
    movies_canvas.configure(yscrollcommand=scrollbar.set)

    show_movies(find_movies_by_cinema(cinema_id.get()), movies_canvas, window, sale)

    window.mainloop()


def show_movie_info(movie: dict, window: tk) -> None:
    frame_movie = tk.Frame(window, bg='#2B2A33')
    frame_movie.pack(pady=10)
    poster_base64_movie = endpoints.get_poster_by_id(movie['poster_id'])
    poster = ImageTk.PhotoImage(decodificar_imagen_base64(poster_base64_movie))

    button_movie = tk.Button(frame_movie, image=poster, bg='#2B2A33')
    button_movie.image = poster  # to prevent garbage collection
    button_movie.pack(side='left', padx=30, pady=20)

    movie_info_frame = tk.Frame(frame_movie, bg='#2B2A33')
    movie_name = movie['name']
    movie_name_label = tk.Label(movie_info_frame, text=movie_name, font=('Calibri', 18, "bold"), bg='#2B2A33',
                               fg='#FFFFFF', anchor='center')
    movie_name_label.pack(pady=(30, 10))

    synopsis = movie['synopsis']
    synopsis_label = tk.Label(movie_info_frame, text=synopsis, font=('Calibri', 10, 'italic'), bg='#2B2A33', fg='#FFFFFF',
                        wraplength=500, justify='center')
    synopsis_label.pack(pady=5, padx=10)

    duration = movie['duration']
    duration_label = tk.Label(movie_info_frame, text=duration, font=('Calibri', 10), bg='#2B2A33', fg='#FFFFFF', anchor='center')
    duration_label.pack(pady=5)

    actors = movie['actors']
    actors_label = tk.Label(movie_info_frame, text=actors, font=('Calibri', 10), bg='#2B2A33', fg='#FFFFFF', anchor='center')
    actors_label.pack(pady=5)

    genre = movie['gender']
    genre_label = tk.Label(movie_info_frame, text=genre, font=('Calibri', 10, 'bold'), bg='#2B2A33', fg='#FFFFFF',
                      anchor='center')
    genre_label.pack(pady=5)

    rating = movie['rating']
    rating_label = tk.Label(movie_info_frame, text=rating, font=('Calibri', 10, 'bold'), bg='#2B2A33', fg='#FFFFFF',
                      anchor='center')
    rating_label.pack(pady=5)
    movie_info_frame.pack(side='right')


def show_room_with_seats(cinema: dict, window: tk, sale: dict) -> None:
    seats = "Asientos disponibles:    " + str(cinema['available_seats'])
    seats_label = tk.Label(window, text=seats, font=('Calibri', 10, 'italic'), bg='#2B2A33', fg='#FFFFFF',
                        highlightthickness=1, padx=10)
    seats_label.pack(pady=(60, 10))

    if cinema['available_seats'] > 0:

        available_seats = int(cinema['available_seats'])
        button_book = tk.Button(window, text="RESERVAR", command=lambda: reservation_window(sale, window,available_seats))
        button_book.configure(
            relief=tk.RAISED,
            bd=3,
            font=('Calibri', 10, 'bold'),
            foreground='#FFFFFF',
            background='grey',
            padx=5,
            pady=5,
        )
        button_book.pack(pady=10)

    else:

        label_texto = 'SALA LLENA - sin asientos disponibles.'
        label = tk.Label(window, text=label_texto, font=('Calibri', 13), bg='#2B2A33', fg='black', foreground='#FFFFFF')
        label.pack(pady=10)


def secondary_window(window_principal: tk, sale: dict, ID_movie: str) -> None:
    window_principal.withdraw()  # Cierra la ventana anterior

    cinema: dict = endpoints.get_cinema_info_by_id(sale['ID_cinema'])
    movie: dict = endpoints.get_movie_by_id(ID_movie)

    # Completo el dict con toda la data elegida por el ususario
    sale['ID_pelicula'] = ID_movie
    sale['nombre_pelicula'] = movie['name']

    window = tk.Toplevel()
    window.geometry("1280x720")
    window.configure(bg='#2B2A33')
    window.title('PANTALLA SECUNDARIA')

    title = cinema['location'].upper()
    title_label = tk.Label(window, text=title, font=("Calibri", 30, "bold", "underline"), bg='#2B2A33', fg='grey',
                      anchor='center')
    title_label.pack(pady=15)

    button_principal_window = tk.Button(window, text=">> Volver a pantalla principal",
                                       command=lambda: [window.withdraw(), principal_window(sale)])
    button_principal_window.configure(
        relief=tk.RAISED,
        bd=3,
        font=('Calibri', 8, 'bold'),
        foreground='#FFFFFF',
        background='black',
        padx=10,
        pady=5,
        anchor='center'
    )
    button_principal_window.pack(pady=10)

    show_movie_info(movie, window)
    show_room_with_seats(cinema, window, sale)

    window.mainloop()


def price_per_ticket(number_box, price, final_price_ticket, text_value=None) -> None:
    number = int(number_box.get())

    if number == 1:
        final_price_ticket = price

    else:
        final_price_ticket: float = (number * price)

    text_value['text'] = f"${final_price_ticket}"


def add_to_cart(number_snack, snacks_box, dict_cart, text_value_2, stock_of_snacks, price, number_box, final) -> None:
    number_snacks = int(number_snack.get())
    snack = str(snacks_box.get())
    # print(snack, number_snacks)

    price_snack = float(stock_of_snacks[snack])  # precio c/u
    price_final_snack = (price_snack * number_snacks)
    # print(price_snack,price_final_snack)
    dict_cart[snack] = (number_snacks, price_final_snack)

    final_price: int = 0

    if number_snacks == 0:
        del dict_cart[snack]

    for key in dict_cart:
        price = float(dict_cart[key][1])
        final_price += price

    final.append(final_price)
    # print(dict_cart)
    text_value_2['text'] = f"{dict_cart} : ${final_price}"


def ticket_confirm(dict_cart, number_box, price, final_price_ticket) -> None:
    number_tickets = number_box.get()
    number_tickets = int(number_tickets)

    final_price_ticket = (number_tickets * price)
    dict_cart['Asientos'] = (number_tickets, final_price_ticket)


def reservation_window(sale: dict, window: tk, available_seats: int) -> None:
    window.withdraw()

    window1 = tk.Tk()
    window1.geometry("1280x720")
    window1.resizable(False, False)
    window1.title('Pantalla de reserva')
    window1.configure(bg='#2b2a33')
    font_type = 'Calibri'

    price = float(sale['precio_entrada'])
    list_names_snacks, list_prices_snacks, list_ult, stock_of_snacks = endpoints.get_stock_snacks()
    final = []
    dict_cart: dict = {}
    final_price_ticket: int = 0

    # titulo principal
    title = tk.Label(
        window1,
        text="🕐 PANTALLA DE RESERVA",
        font=(font_type, 25, "bold"),
        width=25,
        height=2,
        bg='#2b2a33',
        fg='#ffffff'
    )

    title.place(x=450, y=50)

    # titulo secundario asientos
    second_title = tk.Label(
        window1,
        text="🎞️ Cantidad de entradas:",
        font=(font_type, 18),
        width=30,
        height=2,
        bg='#2b2a33',
        fg='#ffffff'
    )

    second_title.place(x=105, y=150)

    # input numero de asientos
    current_value = tk.IntVar()
    number_box = tk.Spinbox(
        window1,
        from_=0,
        to=available_seats,
        textvariable=current_value,
        wrap=True,
        state="readonly",
        font=(font_type, 15),
        command=lambda: price_per_ticket(number_box, price, final_price_ticket, text_value)
    )

    number_box.place(
        x=290,
        y=230,
        width=100,
        height=30
    )

    # precio de las entradas
    text_value = tk.Label(
        window1,
        text="$0.0",
        font=(font_type, 18),
        bg='#2b2a33',
        fg='#ffffff'
    )
    text_value.place(x=170, y=230)

    # boton confirmar aisnetos
    confirm_tickets = tk.Button(
        window1,
        text="CONFIRMAR ENTRADAS",
        font=(font_type, 18),
        command=lambda: ticket_confirm(dict_cart, number_box, price, final_price_ticket)
    )

    confirm_tickets.place(x=210, y=300)

    # tercer titulo snacks
    tird_title = tk.Label(
        window1,
        text="🌭   Agregar Snacks:",
        font=(font_type, 18),
        width=30,
        height=2,
        bg='#2b2a33',
        fg='#ffffff'
    )

    tird_title.place(x=480, y=148)

    # input snaks
    current_var = tk.StringVar()
    snacks_box = ttk.Combobox(
        window1,
        state='readonly',
        values=list_names_snacks,
        textvariable=current_var,
        font=(font_type, 18),
        width=20
    )

    snacks_box.place(
        x=500,
        y=230
    )

    # titulos precios
    text_prices = tk.Label(
        window1,
        text="💰   Lista de precios:",
        font=(font_type, 18),
        width=30,
        height=2,
        bg='#2b2a33',
        fg='#ffffff'
    )

    text_prices.place(x=900, y=148)

    # precios snacks
    list_prices = tk.Listbox(window1, font=(font_type, 18), width=25, height=7)  # height define el numero de filas
    list_prices.insert(0, *list_ult)
    list_prices.place(x=960, y=210)

    # numero del snack
    number_of_snacks = tk.IntVar()
    number_snack = tk.Spinbox(
        window1,
        from_=0,
        to=5,
        textvariable=number_of_snacks,
        wrap=True,
        state="readonly",
        font=(font_type, 18)
    )

    number_snack.place(
        x=800,
        y=233,
        width=100,
        height=30
    )

    # boton agregar snack
    add_botton = tk.Button(
        window1,
        text="¡Agregar al carrito!",
        font=(font_type, 18),
        command=lambda: add_to_cart(number_snack, snacks_box, dict_cart, text_value_2, stock_of_snacks, price,
                                    number_box, final),
    )

    add_botton.place(
        x=550,
        y=300
    )

    # mostrar carrito
    text_value_2 = tk.Label(window1, font=(font_type, 13))
    text_value_2.place(x=20, y=450)

    # boton pagar
    final_button = tk.Button(
        window1,
        font=(font_type, 18, "bold"),
        relief=tk.RAISED,
        bd=3,
        padx=5,
        pady=5,
        text="Checkout/Pagar",
        command=lambda: checkout_window(window1, sale, dict_cart, list_names_snacks)
    )
    final_button.place(x=550, y=600)

    window1.mainloop()


def checkout_window(window1: tk, sale: dict, dict_cart: dict, list_names_snacks: list) -> None:
    window1.withdraw()

    sale['cantidad_entradas'] = dict_cart['Asientos'][0]

    for snack in list_names_snacks:
        if snack in dict_cart:
            sale['snacks'] += [[snack, dict_cart[snack][0], dict_cart[snack][1]]]

    total: int = 0
    total_tickets: int = 0
    total_snacks: int = 0

    window = tk.Tk(screenName='Pantalla Checkout')
    window.geometry("1280x720")
    window.configure(bg='#2B2A33')
    window.title('>>> CHECKOUT')
    
    # Titulo
    title = ' 🛒 '
    title_label = tk.Label(window, text=title, font=("Calibri", 50, "bold"), bg='#2B2A33', fg='white',
                      anchor='center')
    title_label.pack(pady=15)
    title_2 = ' RESUMEN DE COMPRA '
    title_2_label = tk.Label(window, text=title_2, font=("Calibri", 30, "bold"), bg='#2B2A33', fg='white',
                       anchor='center')
    title_2_label.pack(pady=15)

    canvas = tk.Canvas(window, bg='#2B2A33', highlightbackground='#2B2A33')
    canvas.pack(fill='both', padx=60, pady=30)

    # Tickets
    tickets_canvas = tk.Canvas(canvas, bg='#2B2A33', highlightthickness=0)
    tickets_canvas.pack(side=tk.LEFT, expand=1, fill=tk.BOTH, pady=15)
    
    tickets_frame = tk.Frame(tickets_canvas, bg='#2B2A33', highlightbackground='#2B2A33')
    tickets_frame.pack(fill='both')

    title_tickets = ' ENTRADAS '
    title_tickets_label = tk.Label(tickets_frame, text=title_tickets, font=("Calibri", 20, "bold"), bg='white',
                               fg='black', anchor='center')
    title_tickets_label.pack(pady=20)
    movie_title = sale['nombre_pelicula']
    movie_title_label = tk.Label(tickets_frame, text=movie_title, font=("Calibri", 15, "bold"), bg='#2B2A33',
                               fg='white', anchor='center')
    movie_title_label.pack(pady=5)
    number_of_tickets = "- Entradas: " + str(sale['cantidad_entradas'])
    number_of_tickets_label = tk.Label(tickets_frame, text=number_of_tickets, font=("Calibri", 10),
                                        bg='#2B2A33', fg='white', anchor='center')
    number_of_tickets_label.pack(pady=5)
    title_tickets_price = "- Precio Unitario: $" + str(sale['precio_entrada'])
    title_tickets_price_label = tk.Label(tickets_frame, text=title_tickets_price, font=("Calibri", 10),
                                      bg='#2B2A33', fg='white', anchor='center')
    title_tickets_price_label.pack(pady=5)

    total_tickets = sale['cantidad_entradas'] * sale['precio_entrada']

    title_total_tickets = "TOTAL ENTRADAS: $" + str(total_tickets)
    title_total_tickets_label = tk.Label(tickets_frame, text=title_total_tickets, font=("Calibri", 12, "bold"),
                                     bg='black', fg='white', anchor='center')
    title_total_tickets_label.pack(pady=(10, 25))

    # Snacks
    snacks_canvas = tk.Canvas(canvas, bg='#2B2A33', highlightthickness=0)
    snacks_canvas.pack(side=tk.LEFT, expand=1, fill=tk.BOTH, pady=15)
    
    scrollbar = tk.Scrollbar(snacks_canvas, orient="vertical", bg='#2B2A33', command=snacks_canvas.yview)
    scrollbar.pack(side='right', fill='y')
    snacks_canvas.configure(yscrollcommand=scrollbar.set)
    
    snacks_frame = tk.Frame(snacks_canvas, bg='#2B2A33', highlightbackground='#2B2A33')
    snacks_frame.pack(fill='both')
    snacks_canvas.create_window((20, 20), window=snacks_frame, anchor='n')

    title_snacks = ' SNACKS '
    title_snacks_label = tk.Label(snacks_frame, text=title_snacks, font=("Calibri", 20, "bold"), bg='white',
                             fg='black', anchor='center')
    title_snacks_label.grid(row=0, column=1, pady=20)

    index:int = 1

    for snack in sale['snacks']:
        snack_name = "+ " + snack[0]
        snack_name_label = tk.Label(snacks_frame, text=snack_name, font=("Calibri", 15, "bold"),
                                        bg='#2B2A33', fg='white', anchor='center')
        snack_name_label.grid(row=index, column=0, pady=10, padx=5)

        snack_quantity = "Cantidad: " + str(snack[1])
        snack_quantity_label = tk.Label(snacks_frame, text=snack_quantity, font=("Calibri", 10),
                                            bg='#2B2A33', fg='white', anchor='center')
        snack_quantity_label.grid(row=index, column=1, pady=5, padx=5)

        snack_price = "Precio: $" + str(snack[2])
        snack_price_label = tk.Label(snacks_frame, text=snack_price, font=("Calibri", 10),
                                        bg='#2B2A33', fg='white', anchor='center')
        snack_price_label.grid(row=index, column=2, pady=5, padx=5)

        total_snacks += snack[2]
        index +=1
        
    title_total_snacks = "TOTAL SNACKS: $" + str(int(total_snacks))
    title_total_snacks_label = tk.Label(snacks_frame, text=title_total_snacks, font=("Calibri", 12, "bold"),
                                   bg='black', fg='white', anchor='center')
    title_total_snacks_label.grid(row=index, column=1, pady=5)

    snacks_canvas.update_idletasks()  # Update the canvas
    snacks_canvas.config(scrollregion=snacks_canvas.bbox('all'))

    total = total_tickets + total_snacks
    total_text = ' TOTAL: $' + str(int(total))
    total_label = tk.Label(window, text=total_text, font=("Calibri", 25, "bold"), bg='black', fg='white',
                            anchor='center')
    total_label.pack(pady=25)

    pay_button = tk.Button(window, text="PAGAR", command=lambda: payment_window(window, sale))
    pay_button.configure(
        relief=tk.RAISED,
        bd=3,
        font=('Calibri', 15, 'bold'),
        foreground='white',
        background='grey',
        padx=20,
        pady=5,
    )
    pay_button.pack(pady=10)


def generate_QR_pdf(info: str) -> None:
    img_qr = qrcode.make(info)
    img_qr.save("QR_GENERADO.png")

    with open('QR_generado.pdf', 'wb') as pdf_file:
        qr_image = Image.open("QR_GENERADO.png")
        qr_image.save(pdf_file, "pdf")


def button_pay(sale: dict, window2: tk, dict_qr, card_number_input, expiry_input, security_code_input) -> None:
    card_number = str(card_number_input.get())
    expiry = str(expiry_input.get())
    security_code = str(security_code_input.get())

    if len(card_number) != 19 or card_number == '0000-0000-0000-0000' or len(expiry) != 5 or expiry == 'MM/AA' or len(
            security_code) != 3 or security_code == '***':

        messagebox.showinfo(message="Verifique los datos de su tarjeta", title="Error en los datos")

    else:
        locale.setlocale(locale.LC_ALL, '')
        date = datetime.datetime.now()
        timestamp_sale = date.strftime('%d/%m/%Y %H:%M')

        sale['timestamp_sale'] = timestamp_sale

        snacks_final = 0
        for snack in sale['snacks']:
            snacks_final += snack[2]

        final_price_ = (int(sale['cantidad_entradas']) * int(sale['precio_entrada']) + snacks_final)

        id_qr = str(random.randint(1000, 9999)) + str(random.choice(string.ascii_letters))

        sale['ID_QR'] = id_qr

        string_qr = f'{id_qr}; {sale["nombre_pelicula"]}; {sale["ubicacion_totem"]}; {sale["cantidad_entradas"]}; {sale["timestamp_sale"]}; {final_price_}'

        generate_QR_pdf(string_qr)

        dict_ID_QR: dict = {f'{id_qr}': [f'{id_qr}', f'{sale["nombre_pelicula"]}', f'{sale["ubicacion_totem"]}',
                                         f'{sale["cantidad_entradas"]}', f'{sale["timestamp_sale"]}',
                                         f'${final_price_}']}

        with open('IDs_QR.json', 'r') as file_:
            data = json.load(file_)

        data.update(dict_ID_QR)

        with open('IDs_QR.json', 'w') as outfile:
            json.dump(data, outfile, indent=4)

        messagebox.showinfo(message=f"Tu ID de sale es: {id_qr}", title="ID de sale")

        window2.withdraw()


def payment_window(window: tk, sale: dict) -> None:
    window.withdraw()

    window2 = tk.Tk()
    window2.geometry("500x500")
    window2.resizable(False, False)
    window2.title('Pagar/Metodos de pago')
    window2.configure(bg='#2b2a33')

    font_type = 'Calibri'


    payment_methods_label = tk.Label(window2, text='Metodos de pago', font=(font_type, 18), bg='#2b2a33', fg='#ffffff')
    payment_methods_label.place(x=160, y=50)

    payment_methods_list: list = ['Visa', 'Amex', 'MasterCard', 'Naranja', 'Cabal']
    current_var = tk.StringVar()
    payment_methods = ttk.Combobox(
        window2,
        state='readonly',
        values=payment_methods_list,
        textvariable=current_var,
        font=(font_type, 10),
        width=20
    )

    payment_methods.place(x=170, y=100)


    card_number_label = tk.Label(window2, text="Numero de tarjeta", bg='#2b2a33', fg='#ffffff', font=(font_type, 18))
    card_number_label.place(x=160, y=150)

    card_number_input = tk.Entry(window2, width=18, font=(font_type, 13))
    card_number_input.place(x=170, y=200)
    card_number_input.insert(0, "0000-0000-0000-0000")

    security_code_label = tk.Label(window2, text="Codigo de seguridad", bg='#2b2a33', fg='#ffffff',
                                   font=(font_type, 15))
    security_code_label.place(x=50, y=250)

    security_code_input = tk.Entry(window2, width=3, font=(font_type, 13))
    security_code_input.place(x=100, y=300)
    security_code_input.insert(0, "***")

    expiry_label = tk.Label(window2, text='Fecha de vencimiento', bg='#2b2a33', fg='#ffffff', font=(font_type, 15))
    expiry_label.place(x=300, y=250)

    expiry_input = tk.Entry(window2, width=7, font=(font_type, 13))
    expiry_input.place(x=350, y=300)
    expiry_input.insert(0, "MM/AA")

    dict_qr: dict = {}  # diccio solo para generar el qr
    pay_button = tk.Button(
        window2, text='Pagar',
        font=(font_type, 18),
        command=lambda: button_pay(sale, window2, dict_qr, card_number_input, expiry_input, security_code_input),
    )
    pay_button.place(x=210, y=400)

    window2.mainloop()


def main() -> None:
    # Diccionario que guarda toda la info correspondiente a la sale ha realizar. Se utiliza en todas las ventanas.
    sale: dict = {
        'ID_QR': '',
        'ID_pelicula': '',
        'nombre_pelicula': '',
        'ID_cinema': '',
        'ubicacion_totem': '',
        'cantidad_entradas': 0,
        'precio_entrada': 3000,
        'snacks': [],
        'timestamp_sale': ''
    }

    WINDOW.withdraw()

    principal_window(sale)


main()
