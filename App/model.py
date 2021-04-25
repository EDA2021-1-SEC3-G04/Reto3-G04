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

# ==============================
# Construcción de modelos
# ==============================

def newCatalog():
    catalog = {'sentimentvalues': None, 'events': None, 'content_cateogires':None, 'user_created_at': None}
    catalog['events'] = lt.newList('SINGLE_LINKED', cmpEvents)
    catalog['sentimentvalues'] = mp.newMap(numelements=100000, maptype='PROBING', loadfactor=0.5, comparefunction=cmpHashtags)
    catalog['content_cateogries'] = mp.newMap(numelements=17, maptype='PROBING', loadfactor=0.5, comparefunction=cmpCategories)
    catalog['user_created_at'] = om.newMap(omaptype='RBT',
                                      comparefunction=cmpDates)
    catalog['unique_artists'] = mp.newMap(numelements=50000, maptype='CHAINING', loadfactor=0.5,  comparefunction = cmpCategories)
    catalog['unique_tracks'] = mp.newMap(numelements=50000, maptype='CHAINING', loadfactor=0.5, comparefunction = cmpCategories)
    catalog['genre_dictionary'] = mp.newMap(numelements=100, maptype='PROBING', loadfactor=0.5,  comparefunction=cmpCategories)
    return catalog


# =========================================
# Funciones para agregar info al catalogo
# ==========================================

def addEvent(catalog, event):
    """
    """
    lt.addLast(catalog['events'], event)
    mp.put(catalog['unique_artists'], event['artist_id'], event)
    mp.put(catalog['unique_tracks'], event['track_id'], event)
    addCategory(catalog, event)
    return catalog


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
    lt.addLast(event_cols, "instrumentalness")
    lt.addLast(event_cols, "liveness")
    lt.addLast(event_cols, "speechiness")
    lt.addLast(event_cols, "danceability")
    lt.addLast(event_cols, "valence")
    lt.addLast(event_cols, "tempo")
    lt.addLast(event_cols, "acousticness")
    lt.addLast(event_cols, "energy")

    # "instrumentalness","liveness","speechiness","danceability","valence","loudness","tempo","acousticness","energy"

    for event in lt.iterator(event_cols): 
        mp.put(map_cate, event,  None)

    return map_cate


def createCategTree(): 
    tree = om.newMap(omaptype='RBT', comparefunction=cmpCategories2)
    return tree


def addUserInfo(catalog, userInfo): 
    mapDates = catalog["user_created_at"] 
    eventDate = userInfo["created_at"]
    eventDate = datetime.datetime.strptime(eventDate, '%Y-%m-%d %H:%M:%S')
    entry = om.get(mapDates, eventDate.date())
    if entry is None: 
        datentry = lt.newList()
        om.put(mapDates, eventDate.date(), datentry) 
    else:
        datentry = me.getValue(entry)
    
    lt.addLast(datentry, userInfo)
    return catalog


def addHashtag(catalog, event): 
    hashtag = event['hashtag'].lower()
    mp.put(catalog["sentimentvalues"], hashtag,  event['vader_avg'])
    return catalog





# ==============================
# Funciones de Consulta
# ==============================


"""Requerimeinto 1"""
def categoryCaracterization(catalog, categoria, min_range, max_range): 
    category_info = mp.get(catalog['content_cateogries'], categoria)
    category_tree = me.getValue(category_info)
    category_tree['cmpfunction'] = cmpCategories2
    
    list_of_lists = om.values(category_tree, min_range, max_range)
    total = 0
    unique_artists = mp.newMap(numelements=5000, maptype='CHAINING', comparefunction=cmpCategories)
    
    for sub_list in lt.iterator(list_of_lists): 
        for item in lt.iterator(sub_list):
            if checkWithUser(catalog, item): 
                total += 1
                mp.put(unique_artists, item['artist_id'], item)

    artist = mp.size(unique_artists)
    return total, artist

"""Requerimeinto 2"""


def partyMusic(catalog, min_energy, max_energy, min_danceability, max_danceablity): 
    energy_tree = me.getValue(mp.get(catalog['content_cateogries'], 'energy'))

    energy_values = om.values(energy_tree, min_energy, max_energy)

    unique_tracks = mp.newMap(numelements=5000, maptype='CHAINING', comparefunction=cmpCategories)
    final_items = lt.newList(datastructure='ARRAY_LIST')
    for sublist in lt.iterator(energy_values):
        for event in lt.iterator(sublist): 
            if checkWithUser(catalog, event):
                if min_danceability <= float(event['danceability']) <= max_danceablity: 
                    lt.addLast(final_items, event)
                    mp.put(unique_tracks, event['track_id'], event)

    tracks = mp.size(unique_tracks)
    
    return final_items, tracks
                
"""Requerimeinto 3"""
def relaxingMusic(catalog, min_instrumentalness, max_instrumentalness, min_tempo, max_tempo):
    instrumentalness_tree = me.getValue(mp.get(catalog['content_cateogries'], 'instrumentalness'))
    instrumentalness_values = om.values(instrumentalness_tree, min_instrumentalness, max_instrumentalness)

    unique_tracks = mp.newMap(numelements=5000, maptype='CHAINING', comparefunction=cmpCategories)
    final_items = lt.newList(datastructure='ARRAY_LIST')
    for sublist in lt.iterator(instrumentalness_values):
        for event in lt.iterator(sublist): 
            if checkWithUser(catalog, event):
                if min_tempo <= float(event['tempo']) <= max_tempo: 
                    lt.addLast(final_items, event)
                    mp.put(unique_tracks, event['track_id'], event)

    tracks = mp.size(unique_tracks)
    
    return final_items, tracks

def checkWithUser(catalog, event):
    event_date = event['created_at']
    event_date = datetime.datetime.strptime(event_date, '%Y-%m-%d %H:%M:%S')
    user_events_on_date = om.get(catalog['user_created_at'], event_date.date())

    for user_event in lt.iterator(me.getValue(user_events_on_date)):
        if (user_event['user_id'] == event['user_id']) and (user_event['track_id'] == event['track_id']):
            return True
    
    return False


# ==============================
# Funciones de Comparacion
# ==============================


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

def cmpUnique(artist1, artist2): 
    if artist1 < artist2: 
        return -1
    elif artist1 > artist2: 
        return 1
    else: 
        return 0
# Funciones de ordenamiento



 

def countArtist(catalog):
    # TODO: cargar como hashmap y sacar el size
    return mp.size(catalog['unique_artists'])

def countTracks(catalog):
    # TODO: cargar como hashmap y sacar el size
    return mp.size(catalog['unique_tracks'])

def getCateory(catalog, category): 
    category_info = mp.get(catalog['content_cateogries'], category)
    category_tree = None
    if category_info is not None:
        category_tree = me.getValue(category_info)
    return category_tree
    # return om.size(category_tree), om.height(category_tree)
