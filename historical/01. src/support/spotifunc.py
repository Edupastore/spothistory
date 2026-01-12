import os
import json
import pandas as pd
from typing import List, Dict
import spotipy; from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util


def get_streamings(path = '../../02. data/my_spotify_data'):
    """
    Recupera los datos de streaming de archivos JSON en el directorio especificado.

    Args:
        path (str): La ruta al directorio que contiene los archivos JSON de streaming. 
                    Por defecto, '../my_spotify_data'.

    Returns:
        list: Una lista que contiene los datos de streaming recuperados de los archivos JSON.
    """
    files = [os.path.join(path, x)
            for x in os.listdir(path) if x.endswith('.json')]
    
    all_streamings = []

    for file in files:
        try:
            with open(file, 'r', encoding='UTF-8') as f:
                new_streamings = json.load(f)
                all_streamings.extend(new_streamings)
        except Exception as e:
            print(f"Error procesando el archivo {file}: {e}")

    return all_streamings


'''---------------------------------------------------------------------------------------------------------------------'''

def df_summary(df):
    """
    Toma un DataFrame como entrada y devuelve el encabezado, el final, la forma, la información y la suma de valores nulos.

    Args:
        df (DataFrame): El DataFrame de Pandas del que se desea obtener un resumen.

    Returns:
        None: Imprime los resultados directamente.
    """
    
    # Encabezado
    print('\nLos primeros registros:')
    display(df.head())
    print('------------------------------------------------------------------------------------------------------------\n')
    
    # Final
    print('Los últimos registros:')
    display(df.tail())
    print('------------------------------------------------------------------------------------------------------------\n')
    
    # Forma
    print('Número de filas y columnas:')
    display(df.shape)
    print('------------------------------------------------------------------------------------------------------------\n')
    
    # Información
    print('Nombres de las columnas, número de registros no nulos y tipo de dato de cada columna:')
    display(df.info())
    print('------------------------------------------------------------------------------------------------------------\n')
    
    # Suma de valores nulos
    print('Número de registros nulos de cada columna:')
    display(df.isnull().sum())

'''---------------------------------------------------------------------------------------------------------------------''' 

def drop_from_df(df, labels=None, axis=0, index=None, columns=None):
    """
    Elimina filas o columnas de un DataFrame de Pandas y devuelve el DataFrame actualizado.

    Args:
        dataframe: El DataFrame de Pandas al que se le van a aplicar las transformaciones.
        labels: Etiquetas de filas o columnas a eliminar.
        axis: 0 para filas, 1 para columnas.
        index: Sinónimo de labels. Etiquetas de filas a eliminar.
        columns: Sinónimo de labels. Etiquetas de columnas a eliminar.

    Returns:
        El DataFrame de Pandas actualizado después de aplicar las transformaciones.
    """
    data_drop = df.drop(labels=labels, axis=axis, index=index, columns=columns)
    return data_drop

'''---------------------------------------------------------------------------------------------------------------------'''

def cols_location(df):
    """
    Obtiene un diccionario de las columnas de un DataFrame de Pandas
    con las columnas como claves y sus índices como valores.

    Args:
        df (DataFrame): El DataFrame de Pandas del que se desea obtener
        la ubicación de las columnas.

    Returns:
        dictio_cols (dict): Diccionario con las columnas como claves y
        sus índices como valores.
    """
    cols = list(df.columns)
    dictio_cols = {col: i for i, col in enumerate(cols)}
    return dictio_cols

'''---------------------------------------------------------------------------------------------------------------------'''

def value_counts(df, k):
    '''
    Cuenta el número de veces que se repite un mismo valor dentro de una
    columna específica.

    Args:
        df (DataFrame): El DataFrame de entrada.
        k (int): Índice de la columna sobre la que queremos aplicar la función.

    Returns:
        DataFrame: UnaDataFrame que contiene la cuenta de valores únicos en la
        columna especificada.
    '''
    
    if k < 0 or k >= len(df.columns):
        raise ValueError("Índice de columna no válido")

    return pd.DataFrame(df.iloc[:, k].value_counts())

'''---------------------------------------------------------------------------------------------------------------------'''

def unique(df, k):
    '''
    Devuelve el número de observaciones distintas dentro de una columna
    específica.
    
    Args:
        df (DataFrame): El DataFrame de entrada.
        k (int): Índice de la columna sobre la que queremos aplicar la función.

    Returns:
        lista: Una lista que contiene los nombres de los valores únicos
        en la columna especificada.
    '''
    if k < 0 or k >= len(df.columns):
        # Verifica si el índice de la columna es válido.
        raise ValueError("Índice de columna no válido") 
        
    return list(df.iloc[:, k].unique())

'''---------------------------------------------------------------------------------------------------------------------'''



'''---------------------------------------------------------------------------------------------------------------------'''



'''---------------------------------------------------------------------------------------------------------------------'''


        