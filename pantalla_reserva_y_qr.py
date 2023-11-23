import tkinter
from tkinter import ttk
from endpoints import *
import datetime
import locale
import random
import qrcode


def price_per_ticket(current_value, price, final_price_ticket, text_value=None):
    number: int = current_value.get()

    if number == 1:
        final_price_ticket = price

    else:
        final_price_ticket: float = (number * price)


    text_value['text'] = f"${final_price_ticket}"



def add_to_cart(number_of_snacks,snacks_box,dict_cart,text_value_2,stock_of_snacks,price,number_box,final) -> None:
    
    number_snacks:int = number_of_snacks.get() 
    snack:str = snacks_box.get()

    price_snack = float(stock_of_snacks[snack]) #precio c/u
    price_final_snack = (price_snack * number_snacks)

    dict_cart[snack] = (number_snacks,price_final_snack)

    final_price: int = 0

    if number_snacks == 0:
        del dict_cart[snack]

    for key in dict_cart:
        price = float(dict_cart[key][1])
        final_price += price
    
    final.append(final_price)

    text_value_2['text'] = f"{dict_cart} : ${final_price}"


def ticket_confirm(dict_cart,number_box,price,final_price_ticket):

    number_tickets =  number_box.get()
    number_tickets = int(number_tickets)

    final_price_ticket = (number_tickets * price)
    dict_cart['Asientos'] = (number_tickets,final_price_ticket)
    #print(final_price_ticket)



def pantalla_reserva1(dict_entre_ventanas) -> dict:
    window1 = tkinter.Tk()
    window1.geometry("1280x720")
    window1.resizable(False, False)
    window1.title('Pantalla de reserva')
    window1.configure(bg='#2b2a33')
    font_type = 'Calibri'


    price: float = 3000.00  # puse un precio cualquiera, depende de la pelicula en realidad
    list_names_snacks, list_prices_snacks, list_ult, stock_of_snacks = stock_snacks()
    final = []
    dict_cart: dict = {}
    final_price_ticket: int = 0


    # titulo principal
    title = tkinter.Label(
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
    second_title = tkinter.Label(
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
    current_value = tkinter.IntVar(value=0)
    number_box = tkinter.Spinbox(
        window1,
        from_=0,
        to=20,
        textvariable=current_value,
        wrap=True,
        state="readonly",
        font=(font_type, 15),
        command=lambda: price_per_ticket(current_value,price,final_price_ticket,text_value)
        )

    number_box.place(
        x=290,
        y=230,
        width=100,
        height=30
        )

    # precio de las entradas
    text_value = tkinter.Label(
        text="$0.0", 
        font=(font_type, 18),
        bg='#2b2a33',
        fg='#ffffff'
        )
    text_value.place(x=170, y=230)

    # boton confirmar aisnetos
    confirm_tickets = tkinter.Button(
        text="Confirmar Asientos",
        font=(font_type,18), 
        command=lambda: ticket_confirm(dict_cart,number_box,price,final_price_ticket)
        ) 

    confirm_tickets.place(x=210,y= 300)

    # tercer titulo snacks
    tird_title = tkinter.Label(
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
    current_var = tkinter.StringVar()
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
    text_prices = tkinter.Label(
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
    list_prices = tkinter.Listbox(window1,font=(font_type, 18), width= 25, height= 7) # height define el numero de filas
    list_prices.insert(0, *list_ult)
    list_prices.place(x=960,y=210)

    # numero del snack
    number_of_snacks = tkinter.IntVar(value=0)
    number_snack = tkinter.Spinbox(
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
    add_botton = tkinter.Button(
        window1,
        text="¡Agregar al carrito!",
        font=(font_type,18),
        command= lambda: add_to_cart(number_of_snacks,snacks_box,dict_cart,text_value_2,stock_of_snacks,price,number_box,final),
        )

    add_botton.place(
        x=550,
        y=300
        )

    # mostrar carrito
    text_value_2 = tkinter.Label(window1,font=(font_type,13))
    text_value_2.place(x=20, y=450)

    # boton pagar
    final_button = tkinter.Button(
        window1,
        font=(font_type, 18),
        text= "Pagar/Añadir metodo de pago",
        command= lambda:pantalla_reserva2(dict_cart,dict_entre_ventanas,window1)
        )
    final_button.place(x=460, y=600)

    window1.mainloop()

    return dict_cart # quitar


def button_pay(dict_entre_ventanas,window2):

    locale.setlocale(locale.LC_ALL, '')
    fecha_actual = datetime.datetime.now()
    timestamp_compra = fecha_actual.strftime('%d/%m/%Y %H:%M')

    dict_entre_ventanas['timestamp_compra'] = timestamp_compra

    id_qr = random.randint(1000, 9999)

    dict_entre_ventanas['ID_QR'] = id_qr
    
    string_qr: str = ''
    for key in dict_entre_ventanas:
        string_qr += f'{str(dict_entre_ventanas[key])}; '

    img = qrcode.make(string_qr)
    type(img)
    img.save("QR_GENERADO.png")

    window2.withdraw() # cierra la segunda ventana

def pantalla_reserva2(dict_cart,dict_entre_ventanas,window1):

    window1.withdraw() # cierra la primera ventana

    window2 = tkinter.Tk()
    window2.geometry("500x500")
    window2.resizable(False, False)
    window2.title('Pagar/Metodos de pago')
    window2.configure(bg='#2b2a33')

    font_type = 'Calibri'

    dict_entre_ventanas['cantidad_entradas'] = dict_cart['Asientos'][0]

    # boton de pago
    pay_button = tkinter.Button(
        window2, text='Pagar',
         font=(font_type,18),
         command= lambda:button_pay(dict_entre_ventanas,window2),
         )
    pay_button.place(x=190,y= 400)


    # metodos de pago
    payment_methods_label = tkinter.Label(window2,text='Metodos de pago',font=(font_type,18),bg='#2b2a33',fg='#ffffff')
    payment_methods_label.place(x=170,y=50)

    payment_methods_list: list = ['Visa','Amex','MasteCard','Naranja','Cabal']
    current_var = tkinter.StringVar()
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

    card_number_label = tkinter.Label(window2, text="Numero de tarjeta",bg='#2b2a33',fg='#ffffff',font=(font_type,18))    
    card_number_label.place(x=170,y=150)

    card_number_input = tkinter.Entry(window2,width=20,font=(font_type,15))
    card_number_input.place(x=170,y=200)

    security_code_label = tkinter.Label(window2, text="Codigo de seguridad",bg='#2b2a33',fg='#ffffff',font=(font_type,18))
    security_code_label.place(x=170,y=250)

    security_code_input = tkinter.Entry(window2,width=20, font=(font_type,15))
    security_code_input.place(x=170,y=300)


    window2.mainloop()


def main():  # ignorar

    dict_entre_ventanas: dict = {
    'ID_QR':'id generado aleatorio',
    'pelicula': 'nombre pelicula',
    'ubicación_totem':'ubicacion del cine',
    'cantidad_entradas': 0,
    'timestamp_compra': 'hora de la compra'
    }

    print(pantalla_reserva1(dict_entre_ventanas))
    

main()
