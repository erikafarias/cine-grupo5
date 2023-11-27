import tkinter
from tkinter import ttk
from endpoints import *
import datetime
import locale
import random, string
import qrcode
from tkinter import messagebox
import json

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



def pantalla_reserva1(compra) -> None:
    window1 = tkinter.Tk()
    window1.geometry("1280x720")
    window1.resizable(False, False)
    window1.title('Pantalla de reserva')
    window1.configure(bg='#2b2a33')
    font_type = 'Calibri'


    price = float(compra['precio_entrada'])
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
        text= "Checkout/Pagar",
        command= lambda:pantalla_pagar_final(dict_cart,compra,window1,list_names_snacks)
        )
    final_button.place(x=550, y=600)

    window1.mainloop()


def button_pay(compra,window2,dict_qr,card_number_input,expiry_input,security_code_input):

    card_number = str(card_number_input.get())
    expiry = str(expiry_input.get())
    security_code = str(security_code_input.get())

    if len(card_number) != 19 or card_number == '0000-0000-0000-0000' or len(expiry) != 5 or expiry == 'MM/AA' or len(security_code) != 3 or security_code == '***':

        messagebox.showinfo(message="Verifique los datos de su tarjeta", title="Error en los datos")

    else:
        locale.setlocale(locale.LC_ALL, '')
        fecha_actual = datetime.datetime.now()
        timestamp_compra = fecha_actual.strftime('%d/%m/%Y %H:%M')


        compra['timestamp_compra'] = timestamp_compra

        snacks_final = 0
        for snack in compra['snacks']:
            snacks_final += snack[2]

        final_price_ = (int(compra['cantidad_entradas']) * int(compra['precio_entrada']) + snacks_final)
        
        id_qr = str(random.randint(1000, 9999)) + str(random.choice(string.ascii_letters))

        compra['ID_QR'] = id_qr
        
        string_qr = f'{id_qr}; {compra["nombre_pelicula"]}; {compra["ubicacion_totem"]}; {compra["cantidad_entradas"]}; {compra["timestamp_compra"]}; {final_price_}'

        img = qrcode.make(string_qr)
        type(img)
        img.save("QR_GENERADO.png")

        dict_ID_QR: dict = {f'{id_qr}': [f'{id_qr}',f'{compra["nombre_pelicula"]}',f'{compra["ubicacion_totem"]}',f'{compra["cantidad_entradas"]}',f'{compra["timestamp_compra"]}',f'{final_price_}']}

        with open('IDs_QR.json', 'r') as file_:
            data = json.load(file_)

        data.update(dict_ID_QR)

        with open('IDs_QR.json', 'w') as outfile:
            json.dump(data, outfile, indent= 4)

        messagebox.showinfo(message=f"Tu ID de compra es: {id_qr}", title="ID de compra")

        window2.withdraw() # cierra esta ventana

def pantalla_pagar_final(dict_cart,compra,window1,list_names_snacks):

    window1.withdraw() # cierra la primera ventana

    window2 = tkinter.Tk()
    window2.geometry("500x500")
    window2.resizable(False, False)
    window2.title('Pagar/Metodos de pago')
    window2.configure(bg='#2b2a33')

    font_type = 'Calibri'

    # metodos de pago
    payment_methods_label = tkinter.Label(window2,text='Metodos de pago',font=(font_type,18),bg='#2b2a33',fg='#ffffff')
    payment_methods_label.place(x=160,y=50)

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
    card_number_label.place(x=160,y=150)

    card_number_input = tkinter.Entry(window2,width=18,font=(font_type,13))
    card_number_input.place(x=170,y=200)
    card_number_input.insert(0,"0000-0000-0000-0000")
    
    security_code_label = tkinter.Label(window2, text="Codigo de seguridad",bg='#2b2a33',fg='#ffffff',font=(font_type,15))
    security_code_label.place(x=50,y=250)
    
    security_code_input = tkinter.Entry(window2,width=3, font=(font_type,13))
    security_code_input.place(x=100,y=300)
    security_code_input.insert(0,"***")

    expiry_label = tkinter.Label(window2, text='Fecha de vencimiento',bg='#2b2a33',fg='#ffffff',font=(font_type,15))
    expiry_label.place(x=300, y=250)

    expiry_input = tkinter.Entry(window2, width=7, font=(font_type,13))
    expiry_input.place(x=350, y=300)
    expiry_input.insert(0,"MM/AA")


    # boton de pago
    dict_qr: dict = {} #diccio solo para generar el qr
    pay_button = tkinter.Button(
        window2, text='Pagar',
         font=(font_type,18),
         command= lambda:button_pay(compra,window2,dict_qr,card_number_input,expiry_input,security_code_input),
         )
    pay_button.place(x=210,y= 400)

    window2.mainloop()


def main():  # ignorar

    compra: dict = {
        'ID_QR'             : '', # Este arrancatia vacio y se llena una vez realizada la compra y generado el QR
        'ID_pelicula'       : '', # Pelicula elegida por el usuario en la pantalla principal
        'nombre_pelicula'   : '',
        'ubicacion_totem'   : '', # Cine elegido por el usuario en la pantalla principal
        'cantidad_entradas' : 0,
        'precio_entrada'    : 0, # Este ya lo definimos aca hardcodeado
        'snacks'            : [],
        'timestamp_compra'  : '' # Hora de la compra -> Cuando el usuario selecciona "comprar" en la pantalla checkout
    }

    pantalla_reserva1(compra)
    

main()

""" para el 
    
    checkout(dict_cart,compra,window1,list_names_snacks):

        window1.withdraw() # cierra la ventana de reserva

        compra['cantidad_entradas'] = dict_cart['Asientos'][0]

        for snack in list_names_snacks:
            if snack in dict_cart:
                compra['snacks'] += [[ snack , dict_cart[snack][0] , dict_cart[snack][1] ]]

 """