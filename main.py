import endpoints
from utils import decodificar_imagen_base64

import tkinter as tk
from PIL import ImageTk
from tkinter import ttk, messagebox
import datetime
import locale
import random, string
import qrcode # pip install qrcode
import json


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


def find_cinema_id_by_name(cinemas: list[dict], cinema_name: str) -> str:
    for c in cinemas:
        if cinema_name == c['location']:
            return c['cinema_id']


def update_cinema_id(cinema_name: str, cinema_id: tk.StringVar, cinemas_list: list) -> None:
    cinema_id.set(find_cinema_id_by_name(cinemas_list, cinema_name))


def find_movie_by_name(movie_name: str, cinema_id: str, movies_canvas: tk.Canvas, entry: tk.Entry, window:tk, sale: dict) -> list[dict]:
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
                
                button = tk.Button(frame_movie, image=poster_movie, bg='#2B2A33', command = lambda ID_movie = movies[m]['movie_id'] : secondary_window(window, sale, ID_movie))
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
    title_label = tk.Label(master=window, text='Cartelera', font='Calibri 24 bold', bg=bg_color, fg=fg_color)
    title_label.pack()

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
    frame_movie.pack(pady = 10)
    poster_base64_movie = endpoints.get_poster_by_id(movie['poster_id'])
    poster = ImageTk.PhotoImage(decodificar_imagen_base64(poster_base64_movie))
    
    button_movie = tk.Button(frame_movie, image=poster, bg='#2B2A33')
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


def show_room_with_seats(cinema: dict, window: tk, sale: dict) -> None:
      
    asientos_texto = "Asientos disponibles:    " + str(cinema['available_seats'])
    asientos = tk.Label(window, text = asientos_texto, font = ('Calibri', 10, 'italic'), bg='#2B2A33', fg = '#FFFFFF', highlightthickness=1, padx=10)
    asientos.pack(pady = (60, 10))
    
    if cinema['available_seats'] > 0:

        boton_reserva = tk.Button(window, text="RESERVAR", command= lambda:reservation_window(sale,window))
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


def secondary_window(window_principal: tk, sale: dict, ID_movie: str) -> None:
        
    sale['ID_pelicula'] = ID_movie # Guardo el ID de la pelicula en el diccionario que viene del boton seleccionado
    
    window_principal.withdraw() # Cierra la ventana anterior
    
    cinema:dict = endpoints.get_cinema_info_by_id(sale['ID_cinema'])
    movie:dict = endpoints.get_movie_by_id(sale['ID_pelicula'])
    
    window = tk.Toplevel()
    window.geometry("1280x720")
    window.configure(bg='#2B2A33')
    window.title('PANTALLA SECUNDARIA')
    
    # Titulo
    titulo_texto = cinema['location'].upper()
    titulo = tk.Label(window, text = titulo_texto, font = ("Calibri", 30, "bold", "underline"), bg = '#2B2A33', fg = 'grey', anchor='center')
    titulo.pack(pady = 15)
    
    # Boton pantalla principal
    boton_principal_window = tk.Button(window, text=">> Volver a pantalla principal", command= lambda : [window.withdraw(), principal_window(sale)])
    boton_principal_window.configure(
        relief=tk.RAISED,
        bd=3,
        font=('Calibri', 8, 'bold'),
        foreground='#FFFFFF',
        background='black',
        padx=10,
        pady=5,
        anchor='center'
    )
    boton_principal_window.pack(pady = 10)
    
    # Muestro la pelicula elegida
    show_movie_info(movie, window)
    
    # Muestro sala con boton de reserva
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
    
    number_snacks = int(number_snack.get() )
    snack = str(snacks_box.get())
    #print(snack, number_snacks)

    price_snack = float(stock_of_snacks[snack]) #precio c/u
    price_final_snack = (price_snack * number_snacks)
    #print(price_snack,price_final_snack)
    dict_cart[snack] = (number_snacks,price_final_snack)

    final_price: int = 0

    if number_snacks == 0:
        del dict_cart[snack]

    for key in dict_cart:
        price = float(dict_cart[key][1])
        final_price += price
    
    final.append(final_price)
    #print(dict_cart)
    text_value_2['text'] = f"{dict_cart} : ${final_price}"


def ticket_confirm(dict_cart, number_box, price, final_price_ticket) -> None:

    number_tickets =  number_box.get()
    number_tickets = int(number_tickets)

    final_price_ticket = (number_tickets * price)
    dict_cart['Asientos'] = (number_tickets,final_price_ticket)


def reservation_window(sale: dict, window: tk) -> None:
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
        text="Pantalla de reserva",
        font=(font_type, 25),
        width=25,
        height=2,
        bg='#2b2a33',
        fg='#ffffff'
        )

    title.place(x=450, y=50)

    # titulo secundario asientos
    second_title = tk.Label(
        window1, 
        text="¡Seleccione numero de asientos!", 
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
        to=20,
        textvariable=current_value,
        wrap=True,
        state="readonly",
        font=(font_type, 15),
        command=lambda: price_per_ticket(number_box,price,final_price_ticket,text_value)
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
        text="Confirmar Asientos",
        font=(font_type,18), 
        command=lambda: ticket_confirm(dict_cart,number_box,price,final_price_ticket)
        ) 

    confirm_tickets.place(x=210,y= 300)

    # tercer titulo snacks
    tird_title = tk.Label(
        window1, 
        text="¡Agregue Snacks Aqui!", 
        font=(font_type, 18),
        width=30,
        height=2,
        bg='#2b2a33',
        fg='#ffffff'
        )

    tird_title.place(x=480, y=148)

    # input snaks
    current_var = tk.StringVar()
    snacks_box =ttk.Combobox(
        window1,
        state='readonly',
        values= list_names_snacks,
        textvariable=current_var,
        font=(font_type, 18),
        width= 20
    )

    snacks_box.place(
        x=500,
        y=230
    )

    # titulos precios
    text_prices = tk.Label(
        window1,
        text= "Lista de precios", 
        font=(font_type, 18),
        width=30,
        height=2,
        bg='#2b2a33',
        fg='#ffffff'
        )

    text_prices.place(x=900,y=148)

    # precios snacks
    list_prices = tk.Listbox(window1,font=(font_type, 18), width= 25, height= 7) # height define el numero de filas
    list_prices.insert(0, *list_ult)
    list_prices.place(x=960,y=210)

    # numero del snack
    number_of_snacks = tk.IntVar()
    number_snack = tk.Spinbox(
        window1,
        from_=0,
        to=5,
        textvariable=number_of_snacks,
        wrap=True,
        state="readonly",
        font=(font_type,18)
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
        font=(font_type,18),
        command= lambda: add_to_cart(number_snack,snacks_box,dict_cart,text_value_2,stock_of_snacks,price,number_box,final),
        )

    add_botton.place(
        x=550,
        y=300
        )

    # mostrar carrito
    text_value_2 = tk.Label(window1,font=(font_type,13))
    text_value_2.place(x=20, y=450)

    # boton pagar
    final_button = tk.Button(
        window1,
        font=(font_type, 18),
        text= "Checkout/Pagar",
        command= lambda:checkout_window(window1,sale,dict_cart,list_names_snacks)
        )
    final_button.place(x=550, y=600)

    window1.mainloop()


def checkout_window(window1: tk, sale: dict, dict_cart: dict, list_names_snacks: list) -> None:
    
    window1.withdraw() # cierra la ventana de reserva

    sale['cantidad_entradas'] = dict_cart['Asientos'][0]

    for snack in list_names_snacks:
        if snack in dict_cart:
            sale['snacks'] += [[ snack , dict_cart[snack][0] , dict_cart[snack][1] ]]


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
    titulo_pelicula_texto = sale['nombre_pelicula']
    titulo_pelicula = tk.Label(entradas_canvas, text = titulo_pelicula_texto, font = ("Calibri", 15, "bold"), bg= '#2B2A33', fg = 'white', anchor='center')
    titulo_pelicula.pack(pady = 5)
    titulo_cantidad_entradas_texto = "- Entradas: " + str(sale['cantidad_entradas'])
    titulo_cantidad_entradas = tk.Label(entradas_canvas, text = titulo_cantidad_entradas_texto, font = ("Calibri", 10), bg= '#2B2A33', fg = 'white', anchor='center')
    titulo_cantidad_entradas.pack(pady = 5)   
    titulo_entradas_precio_texto = "- Precio Unitario: $" + str(sale['precio_entrada'])
    titulo_entradas_precio = tk.Label(entradas_canvas, text = titulo_entradas_precio_texto, font = ("Calibri", 10), bg= '#2B2A33', fg = 'white', anchor='center')
    titulo_entradas_precio.pack(pady = 5)   
    
    total_entradas = sale['cantidad_entradas']*sale['precio_entrada']
    
    titulo_entradas_total_texto = "TOTAL ENTRADAS: $" + str(total_entradas)
    titulo_entradas_total = tk.Label(entradas_canvas, text = titulo_entradas_total_texto, font = ("Calibri", 12, "bold"), bg = 'black', fg = 'white', anchor='center')
    titulo_entradas_total.pack(pady = (10, 25))  
    
    # Snacks
    snacks_canvas = tk.Canvas(canvas, bg= '#2B2A33', highlightthickness = 3)
    snacks_canvas.pack(side=tk.RIGHT, expand=1, fill=tk.BOTH, pady=15)
    
    titulo_snacks_texto = ' SNACKS '
    titulo_snacks = tk.Label(snacks_canvas, text = titulo_snacks_texto, font = ("Calibri", 20, "bold"), bg = 'white', fg = 'black', anchor='center')
    titulo_snacks.pack(pady = 20)
    
    for snack in sale['snacks']:
        titulo_snack_nombre_texto = "+ " + snack[0]
        titulo_snack_nombre = tk.Label(snacks_canvas, text = titulo_snack_nombre_texto, font = ("Calibri", 15, "bold"), bg= '#2B2A33', fg = 'white', anchor='center')
        titulo_snack_nombre.pack(pady = 10)
        titulo_cantidad_snack_texto = "Cantidad: " + str(snack[1])
        titulo_cantidad_snack = tk.Label(snacks_canvas, text = titulo_cantidad_snack_texto, font = ("Calibri", 10), bg= '#2B2A33', fg = 'white', anchor='center')
        titulo_cantidad_snack.pack(pady = 5)   
        titulo_snack_precio_texto = "Precio: $" + str(snack[2])
        titulo_snack_precio = tk.Label(snacks_canvas, text = titulo_snack_precio_texto, font = ("Calibri", 10), bg= '#2B2A33', fg = 'white', anchor='center')
        titulo_snack_precio.pack(pady = 5)
        
        total_snacks += snack[2]

    
    titulo_snacks_total_texto = "TOTAL SNACKS: $" + str(total_snacks)
    titulo_snacks_total = tk.Label(snacks_canvas, text = titulo_snacks_total_texto, font = ("Calibri", 12, "bold"), bg = 'black', fg = 'white', anchor='center')
    titulo_snacks_total.pack(pady = (10, 25))  
    
    # Total
    total = total_entradas + total_snacks
    
    titulo_total_texto = ' TOTAL: $' + str(total)
    titulo_total = tk.Label(window, text = titulo_total_texto, font = ("Calibri", 25, "bold"), bg = 'black', fg = 'white', anchor='center')
    titulo_total.pack(pady = 30)  
    
    boton_pagar = tk.Button(window, text="PAGAR", command= lambda:payment_window(window,sale))
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
    

def button_pay(sale: dict, window2: tk, dict_qr, card_number_input, expiry_input, security_code_input) -> None:

    card_number = str(card_number_input.get())
    expiry = str(expiry_input.get())
    security_code = str(security_code_input.get())

    if len(card_number) != 19 or card_number == '0000-0000-0000-0000' or len(expiry) != 5 or expiry == 'MM/AA' or len(security_code) != 3 or security_code == '***':

        messagebox.showinfo(message="Verifique los datos de su tarjeta", title="Error en los datos")

    else:
        locale.setlocale(locale.LC_ALL, '')
        fecha_actual = datetime.datetime.now()
        timestamp_sale = fecha_actual.strftime('%d/%m/%Y %H:%M')


        sale['timestamp_sale'] = timestamp_sale

        snacks_final = 0
        for snack in sale['snacks']:
            snacks_final += snack[2]

        final_price_ = (int(sale['cantidad_entradas']) * int(sale['precio_entrada']) + snacks_final)
        
        id_qr = str(random.randint(1000, 9999)) + str(random.choice(string.ascii_letters))

        sale['ID_QR'] = id_qr
        
        string_qr = f'{id_qr}; {sale["nombre_pelicula"]}; {sale["ubicacion_totem"]}; {sale["cantidad_entradas"]}; {sale["timestamp_sale"]}; {final_price_}'

        img = qrcode.make(string_qr)
        type(img)
        img.save("QR_GENERADO.png")

        dict_ID_QR: dict = {f'{id_qr}': [f'{id_qr}',f'{sale["nombre_pelicula"]}',f'{sale["ubicacion_totem"]}',f'{sale["cantidad_entradas"]}',f'{sale["timestamp_sale"]}',f'${final_price_}']}

        with open('IDs_QR.json', 'r') as file_:
            data = json.load(file_)

        data.update(dict_ID_QR)

        with open('IDs_QR.json', 'w') as outfile:
            json.dump(data, outfile, indent= 4)

        messagebox.showinfo(message=f"Tu ID de sale es: {id_qr}", title="ID de sale")

        window2.withdraw() # cierra esta ventana


def payment_window(window: tk, sale: dict) -> None:

    window.withdraw() # cierra la primera ventana

    window2 = tk.Tk()
    window2.geometry("500x500")
    window2.resizable(False, False)
    window2.title('Pagar/Metodos de pago')
    window2.configure(bg='#2b2a33')

    font_type = 'Calibri'

    # metodos de pago
    payment_methods_label = tk.Label(window2,text='Metodos de pago',font=(font_type,18),bg='#2b2a33',fg='#ffffff')
    payment_methods_label.place(x=160,y=50)

    payment_methods_list: list = ['Visa','Amex','MasteCard','Naranja','Cabal']
    current_var = tk.StringVar()
    payment_methods = ttk.Combobox(
        window2,
        state='readonly',
        values=  payment_methods_list,
        textvariable= current_var,
        font=(font_type, 10),
        width= 20
    )

    payment_methods.place(x=170, y=100)

    # inputs numero y codigo de seguridad de la tajeta

    card_number_label = tk.Label(window2, text="Numero de tarjeta",bg='#2b2a33',fg='#ffffff',font=(font_type,18))    
    card_number_label.place(x=160,y=150)

    card_number_input = tk.Entry(window2,width=18,font=(font_type,13))
    card_number_input.place(x=170,y=200)
    card_number_input.insert(0,"0000-0000-0000-0000")
    
    security_code_label = tk.Label(window2, text="Codigo de seguridad",bg='#2b2a33',fg='#ffffff',font=(font_type,15))
    security_code_label.place(x=50,y=250)
    
    security_code_input = tk.Entry(window2,width=3, font=(font_type,13))
    security_code_input.place(x=100,y=300)
    security_code_input.insert(0,"***")

    expiry_label = tk.Label(window2, text='Fecha de vencimiento',bg='#2b2a33',fg='#ffffff',font=(font_type,15))
    expiry_label.place(x=300, y=250)

    expiry_input = tk.Entry(window2, width=7, font=(font_type,13))
    expiry_input.place(x=350, y=300)
    expiry_input.insert(0,"MM/AA")


    # boton de pago
    dict_qr: dict = {} #diccio solo para generar el qr
    pay_button = tk.Button(
        window2, text='Pagar',
         font=(font_type,18),
         command= lambda:button_pay(sale,window2,dict_qr,card_number_input,expiry_input,security_code_input),
         )
    pay_button.place(x=210,y= 400)

    window2.mainloop()


def main() -> None:
    
    # Diccionario que guarda toda la info correspondiente a la sale ha realizar. Se utiliza en todas las ventanas.
    sale: dict = {
        'ID_QR'             : '', # Este arrancatia vacio y se llena una vez realizada la sale y generado el QR
        'ID_pelicula'       : '', # Pelicula elegida por el usuario en la pantalla principal
        'nombre_pelicula'   : '',
        'ubicacion_totem'   : '', # Cine elegido por el usuario en la pantalla principal
        'cantidad_entradas' : 0,
        'precio_entrada'    : 3000, # Este ya lo definimos aca hardcodeado
        'snacks'            : [],
        'timestamp_sale'  : '' # Hora de la sale -> Cuando el usuario selecciona "saler" en la pantalla checkout
    }

    
    WINDOW.withdraw()

    principal_window(sale)

    WINDOW.mainloop()


main()
