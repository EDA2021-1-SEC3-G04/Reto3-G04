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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
import datetime
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

#Construcción de modelos
def newCatalog():
    catalog = {'sentimentvalues': None, 'events': None, 'content_cateogires':None, 'user_created_at': None}
    catalog['events'] = lt.newList('SINGLE_LINKED', cmpEvents)
    catalog['sentimentvalues'] = mp.newMap(numelements=100000, maptype='PROBING', loadfactor=0.5, comparefunction=cmpHashtags)
    catalog['content_cateogries'] = mp.newMap(numelements=17, maptype='PROBING', loadfactor=0.5, comparefunction=cmpCategories)
    catalog['user_created_at'] = om.newMap(omaptype='RBT',
                                      comparefunction=cmpDates)
    return catalog


# Funciones para agregar informacion al catalogo
def addEvent(catalog, event):
    """
    """
    lt.addLast(catalog['events'], event)
    addCategory(catalog, event)
    return catalog
# Funciones para creacion de datos

# Funciones de consulta

def categoryCaracterization(catalog, categoria, min_range, max_range): 
    category_info = mp.get(catalog['content_cateogries'], categoria)

    category_tree = me.getValue(category_info)

    category_tree['cmpfunction'] = cmpCategories
    list_of_lists = om.values(category_tree, min_range, max_range)

    total = 0
    artist_list = lt.newList()
    for sub_list in lt.iterator(list_of_lists): 
        total += lt.size(sub_list)
        for item in lt.iterator(sub_list):
            item_present = lt.isPresent(artist_list, item['artist_id'])
            if item_present == 0:
                lt.addLast(artist_list, item['artist_id'])
    
    artist = lt.size(artist_list)
    return total, artist


# Funciones utilizadas para comparar elementos dentro de una lista

def cmpHashtags(hashtag1, hashtag2):
    hashtag2 = hashtag2['key']
    if hashtag1 > hashtag2: 
        return 1
    if hashtag1 < hashtag2: 
        return -1
    else:
        return 0

def cmpEvents(event1, event2):
    if event1 > event2: 
        return 1
    if event1 < event2: 
        return -1
    else:
        return 0

def cmpCategories(cat1, cat2):
    cat2 = cat2['key']
    if cat1 > cat2: 
        return 1
    if cat1 < cat2: 
        return -1
    else:
        return 0    

def cmpCategories2(cat1, cat2):
    if cat1 > cat2: 
        return 1
    if cat1 < cat2: 
        return -1
    else:
        return 0    
def cmpDates(date1, date2):
    """
    Compara dos fechas
    """
    if (date1 == date2):
        return 0
    elif (date1 > date2):
        return 1
    else:
        return -1   
# Funciones de ordenamiento


def addCategory(catalog, event): 
    category_map = catalog['content_cateogries']
    keys = mp.keySet(category_map)
    if lt.size(keys) <= 0: 
        fillHashMap(category_map)
    keys = mp.keySet(category_map)
    for item in lt.iterator(keys): 
        valor_item = float(event[item])

        cate_tree = me.getValue(mp.get(category_map, item))
        if cate_tree is None: 
            cate_tree = createCategTree()
            mp.put(category_map, item, cate_tree)

        if om.size(cate_tree) == 0:
            tree_list = lt.newList()
            lt.addLast(tree_list, event)
            om.put(cate_tree, valor_item, tree_list)
        else:
            tree_val = om.get(cate_tree, valor_item)
            if tree_val is None:
                tree_list = lt.newList()
                om.put(cate_tree, valor_item, tree_list)
            else:
                tree_list = me.getValue(tree_val)
            
            lt.addLast(tree_list, event)


    return catalog
            

def fillHashMap(map_cate):
    event_cols = lt.newList(datastructure='ARRAY_LIST')
    lt.addLast(event_cols,"instrumentalness")
    lt.addLast(event_cols,"liveness")
    lt.addLast(event_cols,"speechiness")
    lt.addLast(event_cols,"danceability")
    lt.addLast(event_cols,"valence")
    lt.addLast(event_cols,"tempo")
    lt.addLast(event_cols,"acousticness")

    # "instrumentalness","liveness","speechiness","danceability","valence","loudness","tempo","acousticness","energy"
    for event in lt.iterator(event_cols): 
        mp.put(map_cate, event,  None)

    return map_cate

def createCategTree(): 
    tree = om.newMap(omaptype='RBT', comparefunction=cmpCategories2)
    return tree

def addUserInfo(catalog, userInfo): 
    mapDates=catalog["user_created_at"] 
    eventDate = userInfo["created_at"]
    eventDate = datetime.datetime.strptime(eventDate, '%Y-%m-%d %H:%M:%S')
    entry = om.get(mapDates,eventDate.date())
    if entry is None: 
        datentry = lt.newList()
        om.put(mapDates, eventDate.date(), datentry) 
    else:
        datentry = me.getValue(entry)
    
    lt.addLast(datentry, userInfo)
    return catalog

def addHashtag(catalog, event): 
    hashtag = event['hashtag']
    mp.put(catalog["sentimentvalues"], hashtag,  event['vader_avg'])
    return catalog

 

def countArtist(catalog):
    # TODO: cargar como hashmap y sacar el size
    artist_list = lt.newList()
    track_list = lt.newList()

    for event in lt.iterator(catalog['events']):
        artist_present = lt.isPresent(artist_list, event['artist_id'])
        track_present = lt.isPresent(artist_list, event['track_id'])

        if artist_present == 0: 
            lt.addLast(artist_list, event['artist_id'])
        if track_present == 0:
            lt.addLast(track_list, event['track_id'])
    artists_size = lt.size(artist_list)
    tracks_size = lt.size(track_list)
    return artists_size, tracks_size


def getCateory(catalog, category): 
    category_info = mp.get(catalog['content_cateogries'], category)
    category_tree = me.getValue(category_info)

    return om.size(category_tree), om.height(category_tree)
