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
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

#Construcción de modelos
def newCatalog():
    catalog = {'sentimentvalues': None, 'events': None, 'content_cateogires':None, 'user_created_at': None}
    catalog['events'] = lt.newList('SINGLE_LINKED', cmpEvents)
    catalog['sentimentalvalues'] = om.newMap(omaptype='BST',
                                      comparefunction=comparesentimentalvalues)
    catalog['content_cateogries'] = mp.newMap(omaptype='BST',
                                      comparefunction=cmpCateogries)
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

# Funciones utilizadas para comparar elementos dentro de una lista

# Funciones de ordenamiento


def addCategory(catalog, event): 
    # map = map by categoria de contenido
    # keySet()
    # if keySet is empty:  #primer dato
    #   fillHashMap()
    # for item in keySet():
    #   el_arbol = get(map, item)
    #   if el arbol no existe:
    #       crearArbolNuevo()
    #   else:
    #       la_lista_del_arbol = getValue(.get(arbol, event[item])_
    #   lt.addLast(la_lista_del_arbol, event)
    pass

def fillHashMap(map, event ):
    mp.put(map. instrumenta;;l. None)

    

def addUserInfo(catalog, userInfo): 
    mapDates=catalog["user_created_at"] 
    eventDate = userInfo["created_at"]
    eventDate = datetime.datetime.strptime(eventDate, '%Y-%m-%d %H:%M:%S')
    entry = om.get(mapDates,eventDate.date())
    if entry is None: 
        datentry = lt.newList()
        om.put(mapDates, mapDates.date(), datentry) 
    else:
        datentry = me.getValue(entry)
    
    lt.addLast(datentry, userInfo)
    return catalog

def addHashtag(cataog, event): 
    hashtag["content_cateogries"] = event["content_cateogries"]
    catalog["content_cateogries"] = catalog["sentimentalvalues"]
    mp.put(catalog["content_cateogries"], event['vader_avg'])
    return catalog

 
