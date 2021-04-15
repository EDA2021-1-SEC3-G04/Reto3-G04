﻿"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

import config as cf
import sys
import controller
from DISClib.ADT import list as lt
assert cf


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""
def printMenu():
    print("\n")
    print("*******************************************")
    print("Bienvenido")
    print("1- Crear catalogo")
    print("2- Cargar información en el catálogo")
    print("3- Caracterizar las reproducciones")
    print("4- Encontrar música para festejar")
    print("5- Encontrar música para estudiar")
    print("6- Estudiar los géneros musicales")
    print("7- Indicar el género musical más escuchado en el tiempo")
    print("8- Salir")
    print("*******************************************")


catalog = None

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        print("\nInicializando....")
        catalog = controller.init()

    elif int(inputs[0]) == 2:
        print("Cargando información de los archivos ....")

    elif int(inputs[0]) == 3:
        pass

    elif int(inputs[0]) == 4:
        pass

    elif int(inputs[0]) == 5:
        pass

    elif int(inputs[0]) == 6:
        pass
    elif int(inputs[0]) == 7:
        pass
    else:
        sys.exit(0)
sys.exit(0)
