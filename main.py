import tkinter as tk
from PIL import ImageTk
import endpoints
from utils import decodificar_imagen_base64


def mostrar_pelicula(movie:dict, window:tk, movie_poster:str) -> None:
    
    poster = ImageTk.PhotoImage(decodificar_imagen_base64(movie_poster))
    poster_label = tk.Label(window, image=poster, bg='black')
    poster_label.pack(pady = 10)
    
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


def mostrar_sala(cinema:dict, window:tk) -> None:
      
    asientos_texto = "Asientos disponibles:    " + str(cinema['available_seats'])
    asientos = tk.Label(window, text = asientos_texto, font = ('Calibri', 10, 'italic'), bg='#2B2A33', fg = '#FFFFFF', highlightthickness=1, padx=10)
    asientos.pack(pady = (60, 10))
    
    if cinema['available_seats'] > 0:

        boton_reserva = tk.Button(window, text="RESERVAR", command='pantalla_reserva()')
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


def pantalla_secundaria(window_principal:tk, ID_cinema:str, ID_pelicula:str) -> None:
    
    window_principal.withdraw() # Cierra la ventana anterior
    
    cinema:dict = endpoints.get_cinema_info_by_id(ID_cinema)
    movie:dict = endpoints.get_movie_by_id(ID_pelicula)
    movie_poster:str = endpoints.get_poster_by_id(movie['poster_id'])['poster_image']
    
    window = tk.Tk(screenName='Pantalla Secundaria')
    window.geometry("1280x720")
    window.configure(bg='#2B2A33')
    window.title('PANTALLA SECUNDARIA')
    
    # Titulo
    titulo_texto = cinema['location'].upper()
    titulo = tk.Label(window, text = titulo_texto, font = ("Calibri", 30, "bold", "underline"), bg = '#2B2A33', fg = 'grey', anchor='center')
    titulo.pack(pady = 15)
    
    # Boton pantalla principal
    boton_pantalla_principal = tk.Button(window, text=">> Volver a pantalla principal", command='pantalla_principal()')
    boton_pantalla_principal.configure(
        relief=tk.RAISED,
        bd=3,
        font=('Calibri', 8, 'bold'),
        foreground='#FFFFFF',
        background='black',
        padx=10,
        pady=5,
        anchor='center'
    )
    boton_pantalla_principal.pack(pady = 10)
    
    # Muestro la pelicula elegida
    mostrar_pelicula(movie, window, movie_poster)
    
    # Muestro sala con boton de reserva
    mostrar_sala(cinema, window)

    window.mainloop()


def pantalla_checkout(window_reserva:tk, compra:dict) -> None:
    
    window_reserva.withdraw() # Cierra la ventana anterior
    
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
    titulo_pelicula_texto = compra['nombre_pelicula']
    titulo_pelicula = tk.Label(entradas_canvas, text = titulo_pelicula_texto, font = ("Calibri", 15, "bold"), bg= '#2B2A33', fg = 'white', anchor='center')
    titulo_pelicula.pack(pady = 5)
    titulo_cantidad_entradas_texto = "- Entradas: " + str(compra['cantidad_entradas'])
    titulo_cantidad_entradas = tk.Label(entradas_canvas, text = titulo_cantidad_entradas_texto, font = ("Calibri", 10), bg= '#2B2A33', fg = 'white', anchor='center')
    titulo_cantidad_entradas.pack(pady = 5)   
    titulo_entradas_precio_texto = "- Precio Unitario: $" + str(compra['precio_entrada'])
    titulo_entradas_precio = tk.Label(entradas_canvas, text = titulo_entradas_precio_texto, font = ("Calibri", 10), bg= '#2B2A33', fg = 'white', anchor='center')
    titulo_entradas_precio.pack(pady = 5)   
    
    total_entradas = compra['cantidad_entradas']*compra['precio_entrada']
    
    titulo_entradas_total_texto = "TOTAL ENTRADAS: $" + str(total_entradas)
    titulo_entradas_total = tk.Label(entradas_canvas, text = titulo_entradas_total_texto, font = ("Calibri", 12, "bold"), bg = 'black', fg = 'white', anchor='center')
    titulo_entradas_total.pack(pady = (10, 25))  
    
    # Snacks
    snacks_canvas = tk.Canvas(canvas, bg= '#2B2A33', highlightthickness = 3)
    snacks_canvas.pack(side=tk.RIGHT, expand=1, fill=tk.BOTH, pady=15)
    
    titulo_snacks_texto = ' SNACKS '
    titulo_snacks = tk.Label(snacks_canvas, text = titulo_snacks_texto, font = ("Calibri", 20, "bold"), bg = 'white', fg = 'black', anchor='center')
    titulo_snacks.pack(pady = 20)
    
    for snack in compra['snacks']:
        titulo_snack_nombre_texto = "+ " + snack[0]
        titulo_snack_nombre = tk.Label(snacks_canvas, text = titulo_snack_nombre_texto, font = ("Calibri", 15, "bold"), bg= '#2B2A33', fg = 'white', anchor='center')
        titulo_snack_nombre.pack(pady = 10)
        titulo_cantidad_snack_texto = "Cantidad: " + str(snack[1])
        titulo_cantidad_snack = tk.Label(snacks_canvas, text = titulo_cantidad_snack_texto, font = ("Calibri", 10), bg= '#2B2A33', fg = 'white', anchor='center')
        titulo_cantidad_snack.pack(pady = 5)   
        titulo_snack_precio_texto = "Precio: $" + str(snack[1]*snack[2])
        titulo_snack_precio = tk.Label(snacks_canvas, text = titulo_snack_precio_texto, font = ("Calibri", 10), bg= '#2B2A33', fg = 'white', anchor='center')
        titulo_snack_precio.pack(pady = 5)
        
        total_snacks += snack[1]*snack[2]

    
    titulo_snacks_total_texto = "TOTAL SNACKS: $" + str(total_snacks)
    titulo_snacks_total = tk.Label(snacks_canvas, text = titulo_snacks_total_texto, font = ("Calibri", 12, "bold"), bg = 'black', fg = 'white', anchor='center')
    titulo_snacks_total.pack(pady = (10, 25))  
    
    # Total
    total = total_entradas + total_snacks
    
    titulo_total_texto = ' TOTAL: $' + str(total)
    titulo_total = tk.Label(window, text = titulo_total_texto, font = ("Calibri", 25, "bold"), bg = 'black', fg = 'white', anchor='center')
    titulo_total.pack(pady = 30)  
    
    boton_pagar = tk.Button(window, text="PAGAR", command='Aca iria la funcion para crear el QR')
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
    

def main() -> None:
    
    # Diccionario que guarda toda la info correspondiente a la compra ha realizar. Se utiliza en todas las ventanas.
    compra: dict = {
        'ID_QR'             : '', # Este arrancatia vacio y se llena una vez realizada la compra y generado el QR
        'ID_pelicula'       : '2', # Pelicula elegida por el usuario en la pantalla principal
        'nombre_pelicula'   : '',
        'ID_cinema'         : '2', # Cine elegido por el usuario en la pantalla principal
        'cantidad_entradas' : 0,
        'precio_entrada'    : 0, # Este ya lo definimos aca hardcodeado
        'snacks'            : [ ['nombre snack', 'cantidad', 'precio unitario'] , ["nombre snack", 'cantidad', 'precio unitario'] ],
        'timestamp_compra'  : '' # Hora de la compra -> Cuando el usuario selecciona "comprar" en la pantalla checkout
    }

    pantalla_secundaria(window_principal, compra['ID_cinema'], compra['ID_pelicula'])
    pantalla_checkout(window_reserva, compra)


main()
