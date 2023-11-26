import endpoints # Funciones para interactuar con la API
from utils import decodificar_imagen_base64 # Funcion para decodificar la imagen de cada pelicula

import tkinter as tk
from PIL import ImageTk



def main() -> None:
    
    # Diccionario que guarda toda la info correspondiente a la compra ha realizar. Se utiliza en todas las ventanas.
    compra: dict = {
        'ID_QR'             : '', # Este arrancatia vacio y se llena una vez realizada la compra y generado el QR
        'ID_pelicula'       : '', # Pelicula elegida por el usuario en la pantalla principal
        'nombre_pelicula'   : '',
        'ubicacion_totem'   : '', # Cine elegido por el usuario en la pantalla principal
        'cantidad_entradas' : 0,
        'precio_entrada'    : 0, # Este ya lo definimos aca hardcodeado
        'snacks'            : [ ['nombre snack', 'cantidad', 'precio unitario'] , ["nombre snack", 'cantidad', 'precio unitario'] ],
        'timestamp_compra'  : '' # Hora de la compra -> Cuando el usuario selecciona "comprar" en la pantalla checkout
    }


main()