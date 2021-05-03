"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
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
import model
import csv
import time
import tracemalloc

"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de libros

def init(): 
    catalog = model.newCatalog()
    return catalog

# Funciones para la carga de datos

def loadData(catalog, contextcontentfile, sentimentvaluesfile, userhashtagsfile):
    delta_time = -1.0
    delta_memory = -1.0
    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()

    loadContext(catalog, contextcontentfile)
    loadUserTrackHashtag(catalog, userhashtagsfile)
    loadSentimentValues(catalog, sentimentvaluesfile)
    artists = model.countArtist(catalog)
    tracks = model.countTracks(catalog)

    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()
    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)
    
    return catalog, artists, tracks, delta_time, delta_memory


def loadSentimentValues(catalog, sentimentvaluesfile):
    sentimentvaluesfile = cf.data_dir + sentimentvaluesfile
    input_file = csv.DictReader(open(sentimentvaluesfile, encoding="utf-8"),
                                delimiter=",")
    for hashtag in input_file:
        model.addHashtag(catalog, hashtag)
    return catalog

def loadContext(catalog, contextcontefile): 
    contextcontentfile = cf.data_dir + contextcontefile
    input_file = csv.DictReader(open(contextcontentfile, encoding="utf-8"),
                                delimiter=",")
    for event in input_file:
        model.addEvent(catalog, event)
    return catalog

def loadUserTrackHashtag(catalog, userhashtagsfile): 
    userhashtagsfile = cf.data_dir + userhashtagsfile
    input_file = csv.DictReader(open(userhashtagsfile, encoding="utf-8"),
                                delimiter=",")
    for date in input_file:
        model.addUserInfo(catalog, date)
    return catalog

# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo"""

def categoryCaracterization(catalog, categoria, min_range, max_range):
    return model.categoryCaracterization(catalog, categoria, min_range, max_range)

def partyMusic(catalog, min_energy, max_energy, min_danceability, max_danceablity):
    return model.partyMusic(catalog, min_energy, max_energy, min_danceability, max_danceablity)

def getCateory(catalog, category): 
    return model.getCateory(catalog, category)

def relaxingMusic(catalog, min_instrumentalness, max_instrumentalness, min_tempo, max_tempo):
    return model.relaxingMusic(catalog, min_instrumentalness, max_instrumentalness, min_tempo, max_tempo)

def newGenre(catalog, name, min_tempo, max_tempo):
    return model.newGenre(catalog, name, min_tempo, max_tempo)

def genreStudy(catalog, genres):
    return model.genresStudy(catalog, genres)
    


def listSize(lst): 
    return model.listSize(lst)

def mapSize(mps): 
    return model.mapSize(mps)

def getReps(answer): 
    return model.getReps(answer)
    
def getGenre(catalog, genre):
    return model.getGenre(catalog, genre)

def genreMostListened(catalog, min_time, max_time): 
    return model.genreMostListened(catalog, min_time, max_time)


# ======================================
# Funciones para medir tiempo y memoria
# ======================================


def getTime():
    """
    devuelve el instante tiempo de procesamiento en milisegundos
    """
    return float(time.perf_counter()*1000)


def getMemory():
    """
    toma una muestra de la memoria alocada en instante de tiempo
    """
    return tracemalloc.take_snapshot()


def deltaMemory(start_memory, stop_memory):
    """
    calcula la diferencia en memoria alocada del programa entre dos
    instantes de tiempo y devuelve el resultado en bytes (ej.: 2100.0 B)
    """
    memory_diff = stop_memory.compare_to(start_memory, "filename")
    delta_memory = 0.0

    # suma de las diferencias en uso de memoria
    for stat in memory_diff:
        delta_memory = delta_memory + stat.size_diff
    # de Byte -> kByte
    delta_memory = delta_memory/1024.0
    return delta_memory
