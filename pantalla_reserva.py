import tkinter
from tkinter import *
import endpoints_nacho
from endpoints_nacho import *

stock_of_snacks: list = stock_snacks()


def price_per_ticket(current_value, price, text_value=None):
    number: int = current_value.get()

    if number == 1:
        final_price = price
        print(final_price)
    else:
        final_price: float = (number * price)
        print(final_price)

    text_value['text'] = f"{final_price}"


def pantalla_reserva1(price: float) -> None:
    window = tkinter.Tk()
    window.geometry("800x600")
    window.resizable(False, False)
    window.title('Pantalla de reserva')

    # titulo principal
    title = tkinter.Label(window, text="Pantalla de reserva")
    title.place(x=330, y=50)

    # titulo secundario
    second_title = tkinter.Label(window, text="Seleccionar numero de asientos y precio")
    second_title.place(x=270, y=100)

    # input numero de asientos
    current_value = tkinter.IntVar(value=0)
    spin_box = tkinter.Spinbox(
        window,
        from_=0,
        to=50,
        textvariable=current_value,
        wrap=True,
        state="readonly",
        command=lambda: price_per_ticket(current_value, price, text_value))

    spin_box.place(
        x=400,
        y=150,
        width=50)

    text_value = tkinter.Label()
    text_value.place(x=300, y=150)

    window.mainloop()


def main():  # ignorar
    price: float = 3000.00  # puse un precio cualquiera, depende de la pelicula en realidad
    pantalla_reserva1(price)


main()
