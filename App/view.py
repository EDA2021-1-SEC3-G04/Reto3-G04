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
import random
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
    print("0- Salir")
    print("*******************************************")


def printLoadInfo(answer):
    catalog = answer[0]
    print("Total eventos de escucha:", lt.size(catalog['events']))
    print("Total eventos de artistas unicos:", answer[1])
    print("Total eventos de tracks unicos:", answer[2], '\n')

    sub_list1 = lt.subList(catalog['events'], 1, 5)
    sub_list2 = lt.subList(catalog['events'], lt.size(catalog['events']) - 6, 5)

    n = 1
    for item in lt.iterator(sub_list1): 
        print('Video', n, ':', item, '\n')
        n += 1
    for item in lt.iterator(sub_list2): 
        print('Video', n, ':', item, '\n')
        n += 1


def printTracks(list_of_tracks): 
    print('\n--- Unique track_id ---')
    statement = 'Track {}: {} with energy of {} and danceability of {}'
    for n in range(0, 5): 
        random_pos = random.randint(1, lt.size(list_of_tracks))
        rand_item = lt.getElement(list_of_tracks, random_pos)

        print(statement.format(n, rand_item['track_id'], rand_item['energy'], rand_item['danceability']))

catalog = None

# File names
contextcontentfile ='/subsamples-small/context_content_features-small.csv'
sentimentvaluesfile = '/subsamples-small/sentiment_values.csv'
usertrackhashtagtimestampsfile = '/subsamples-small/user_track_hashtag_timestamp-small.csv'


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
        answer = controller.loadData(catalog, contextcontentfile, sentimentvaluesfile, usertrackhashtagtimestampsfile)
        printLoadInfo(answer)       

    elif int(inputs[0]) == 3:
        category = input('Qué categoria de contenido desea consultar: ')
        category_tree = controller.getCateory(catalog, category)

        if category_tree is not None:
            min_range = float(input('Valor minimo (debe ser entre 0.0 y 1.0): '))
            max_range = float(input('Valor maximo (debe ser entre 0.0 y 1.0): '))
            
            if (min_range - max_range > 0.0) or min_range < 0.0 or max_range > 1.0: 
                print('Rangos inválidos, inténtelo de nuevo')
            else: 
                answer = controller.categoryCaracterization(catalog, category, min_range, max_range)

                print('++++++ Req No. 1 results... ++++++')
                statement1 = "{} is between {} and {}"
                statement2 = "Total of reproduction: {} \t Total unique artists {}"
                # print("Para arbol de ", category, "\nElementos:", tree[0], "\nAltura:", tree[1])
                print(statement1.format(category, min_range, max_range))
                print(statement2.format(answer[0], answer[1]))
        else: 
            print('Categoría de contenido no válida')
    elif int(inputs[0]) == 4:
        min_energy = float(input('Valor mínimo para Energy (debe ser entre 0.0 y 1.0): '))
        max_energy = float(input('Valor máximo para Energy (debe ser entre 0.0 y 1.0): '))
        min_danceability = float(input('Valor mínimo para Danceability (debe ser entre 0.0 y 1.0): '))
        max_danceability = float(input('Valor mínimo para Danceability (debe ser entre 0.0 y 1.0): '))

        if (min_energy - max_energy > 0.0) or min_energy < 0.0 or max_energy > 1.0 or (min_danceability - max_danceability > 0.0) or min_danceability < 0.0 or max_danceability > 1:
            print('Rangos inválidos, inténtelo de nuevo')
        else:
            answer = controller.partyMusic(catalog, min_energy, max_energy, min_danceability, max_danceability)

            print('\n \n++++++ Req No. 2 results... ++++++')
            print('Energy is between', min_energy, 'and', max_energy)
            print('Danceability is between', min_danceability, 'and', max_danceability)
            print('Total of unique tracks in events:', answer[1])
            printTracks(answer[0])

    elif int(inputs[0]) == 5:
        pass

    elif int(inputs[0]) == 6:
        pass
    elif int(inputs[0]) == 7:
        pass
    else:
        sys.exit(0)
sys.exit(0)
