import tkinter
from tkinter import ttk

from endpoints import *

list_names_snacks, list_prices_snacks, list_ult, stock_of_snacks = stock_snacks()
#print(list_names_snacks,list_prices_snacks)
#print(list_ult)
#print(stock_of_snacks)

def price_per_ticket(current_value, price, final_price_ticket, text_value=None):
    number: int = current_value.get()

    if number == 1:
        final_price_ticket = price
        #  print(final_price)
    else:
        final_price_ticket: float = (number * price)
        #  print(final_price)

    text_value['text'] = f"${final_price_ticket}"



def add_to_cart(number_of_snacks,window,dict_cart,text_value_2,stock_of_snacks,price,number_box) -> None:
    
    number_snacks:int = number_of_snacks.get() 
    snack:str = window.selected_snack.get()

    price_snack = float(stock_of_snacks[snack]) #precio c/u
    price_final_snack = (price_snack * number_snacks)

    dict_cart[snack] = (number_snacks,price_final_snack)

    final_price: int = 0

    for key in dict_cart:
        price = float(dict_cart[key][1])
        final_price += price
    

    text_value_2['text'] = f"{dict_cart} : ${final_price}"
    #print(dict_cart)


def ticket_confirm(dict_cart,number_box,price,final_price_ticket):

    number_tickets =  number_box.get()
    number_tickets = int(number_tickets)

    final_price_ticket = (number_tickets * price)
    dict_cart['Asientos'] = (number_tickets,final_price_ticket)
    #print(final_price_ticket)



def pantalla_reserva1(price: float, list_names_snacks, list_prices_snacks, list_ult) -> dict:
    window = tkinter.Tk()
    window.geometry("1280x720")
    window.resizable(False, False)
    window.title('Pantalla de reserva')

    dict_cart: dict = {}
    final_price_ticket: int = 0

    # titulo principal
    title = tkinter.Label(window, text="Pantalla de reserva", font=("verdana", 15))
    title.place(x=550, y=50)

    # titulo secundario asientos
    second_title = tkinter.Label(window, text="¡Seleccione numero de asientos!", font=("verdana", 10))
    second_title.place(x=105, y=150)
    


    # input numero de asientos


    current_value = tkinter.IntVar(value=0)
    number_box = tkinter.Spinbox(
        window,
        from_=0,
        to=50,
        textvariable=current_value,
        wrap=True,
        state="readonly",
        command=lambda: price_per_ticket(current_value,price,final_price_ticket,text_value)
        )

    number_box.place(
        x=220,
        y=200,
        width=100,
        height=30
        )

    text_value = tkinter.Label(text="$0.0", font=("ventada", 10))
    text_value.place(x=125, y=205)

    # boton confirmar aisnetos

    confirm_tickets = tkinter.Button(text="Confirmar Asientos", command=lambda: ticket_confirm(dict_cart,number_box,price,final_price_ticket)) 
    confirm_tickets.place(x=170,y= 250)


    # tercer titulo snacks

    tird_title = tkinter.Label(window, text="¡Agrege Snacks Aqui!", font=("ventada", 10))
    tird_title.place(x=500, y=150)


    # input snaks
    window.opcions = list_names_snacks
    window.selected_snack = tkinter.StringVar(window)
    window.prices = list_prices_snacks

    snacks_box =ttk.OptionMenu(
        window,
        window.selected_snack,
        window.opcions[0],
        *window.opcions,
    )

    snacks_box.place(
        x=550,
        y=210
    )

    # precio snack


    text_prices = tkinter.Label(text= "Lista de precios:", font=("ventada", 15))
    text_prices.place(x=950,y =130)

    

    list_prices = tkinter.Listbox(window,font=("ventada", 15), width= 24, height= 7)
    list_prices.insert(0, *list_ult)
    list_prices.place(x=950,y=200)




    # numero del snack
    
    number_of_snacks = tkinter.IntVar(value=0)
    number_snack = tkinter.Spinbox(
        window,
        from_=0,
        to=5,
        textvariable=number_of_snacks,
        wrap=True,
        state="readonly",
        )

    number_snack.place(
        x=420,
        y=205,
        width=100,
        height=30
        )


    # boton agregar snack

    add_botton = ttk.Button(
        text="¡Agregar al carrito!", 
        command= lambda: add_to_cart(number_of_snacks,window,dict_cart,text_value_2,stock_of_snacks,price,number_box),
        )

    add_botton.place(
        x=670,
        y=210
        )

    # mostrar carrito

    text_value_2 = tkinter.Label(window,font=("ventada",15))
    text_value_2.place(x=100, y=350)

    window.mainloop()

    return dict_cart


def main():  # ignorar
    price: float = 3000.00  # puse un precio cualquiera, depende de la pelicula en realidad

    print(pantalla_reserva1(price, list_names_snacks,list_prices_snacks,list_ult))
    

main()
