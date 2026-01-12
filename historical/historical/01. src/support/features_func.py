import os
import json
import pandas as pd
from typing import List, Dict
import spotipy; from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util
from spotipy.exceptions import SpotifyException

def spotify_connection(file_path):
    """
    Crea una conexión con la API de Spotify utilizando las credenciales proporcionadas en un archivo de texto.

    Args:
        file_path (str): Ruta al archivo de texto que contiene el ID de cliente y el secreto de cliente.


    Devuelve
    -------
    sp : spotipy.Spotify
        Objeto de conexión a la API de Spotify.
    """
    with open(file_path, 'r') as file:
        client_id = file.readline().strip()
        client_secret = file.readline().strip()

    auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    sp = spotipy.Spotify(auth_manager=auth_manager)
    return sp

# Crear una instancia de spotipy.Spotify utilizando spotify_connection
sp = spotify_connection('credentials.txt')

'''---------------------------------------------------------------------------------------------------------------------'''

def get_artist_id(tracks_id, sp=sp):
    """
    Extracts the artist_id for each track_id from Spotify.

    Args:
    tracks_id (list): List of track IDs.
    sp: Authenticated Spotipy object.

    Returns:
    list: List of artist IDs associated with each track ID.
    """
    artist_ids = []
    
    for track_id in tracks_id:
        try:
            # Obtener la información de la pista
            track_info = sp.track(track_id)
            # Obtener el ID del primer artista asociado a la pista
            artist_id = track_info['artists'][0]['id']
            artist_ids.append(artist_id)

        except Exception as e:
            print(f"Error processing track {track_id}: {e}")

    return artist_ids

'''---------------------------------------------------------------------------------------------------------------------'''

def get_followers(tracks_id, function=get_artist_id, sp=sp):
    """
    Get the followers count for each artist associated with the given artist
    IDs from Spotify.

    Args:
        tracks_id (list): List of track IDs.
        function: Function to retrieve artist IDs associated with track IDs.
        sp: Authenticated Spotipy object.

    Returns:
        list: List of followers count for each artist ID. Returns None if no
        followers count is found for any artist.
    """
    
    artist_ids = get_artist_id(tracks_id, sp=sp)
    if not artist_ids:
        return None
    
    followers = []

    for artist_id in artist_ids:
        try:
            # Obtener la información del artista
            artist_info = sp.artist(artist_id)
            # Obtener el número total de seguidores del artista
            followers_count = artist_info.get("followers", {}).get("total", None)
            if followers_count is not None:
                followers.append(int(followers_count))
                
        except Exception as e:
            print(f"Error processing track ID {artist_id}: {e}")

    return followers

'''---------------------------------------------------------------------------------------------------------------------'''

def get_top_tracks_id(tracks_id, function=get_artist_id, sp=sp):
    """
    Get the top tracks for each artist associated with the given track IDs from Spotify.

    Args:
    tracks_id (list): List of track IDs.
    function: Function to retrieve artist IDs associated with track IDs.
    sp: Authenticated Spotipy object.

    Returns:
    Tuple: Two lists containing the top tracks IDs and names for each artist associated with the track IDs.
           The first list contains the track IDs and the second list contains the track names.
           Returns None if no artist IDs are found.
    """
    artist_ids = get_artist_id(tracks_id, sp=sp)
    if not artist_ids:
        return None, None
    
    top_tracks_ids = []
    top_tracks_names = []
    for artist_id in artist_ids:
        try:
            top_tracks_info = sp.artist_top_tracks(artist_id)
            for track in top_tracks_info['tracks']:
                top_tracks_ids.append(track['id'])
                top_tracks_names.append(track['name'])
            
        except SpotifyException as e:
            print(f"Error getting top tracks for the artist with ID {artist_id}: {e}")
    
    return top_tracks_ids, top_tracks_names

'''---------------------------------------------------------------------------------------------------------------------'''

def get_release_year(tracks_id, sp=sp):
    """
    Get the release year for each track ID from Spotify.

    Args:
    tracks_id (list): List of track IDs.
    sp: Authenticated Spotipy object.

    Returns:
    list: List of release years associated with each track ID.
    """
    release_years = []
    
    for track_id in tracks_id:
        try:
            # Obtener la información de la pista
            track_info = sp.track(track_id)     
            # Obtener la fecha de lanzamiento del álbum al que pertenece la pista
            release_date = track_info['album']['release_date']    
            # Extraer el año de la fecha de lanzamiento
            release_year = int(release_date.split('-')[0])
            # Agregar el año de lanzamiento a la lista
            release_years.append(release_year)

        except Exception as e:
            print(f"Error getting release year for track {track_id}: {e}")
            return None
        
    return release_years

'''---------------------------------------------------------------------------------------------------------------------'''

def get_track_genres(tracks_id, sp=sp):
    """
    Get the genres for each track ID from Spotify.

    Args:
        tracks_id (list): List of track IDs.
        sp: Authenticated Spotipy object.

    Returns:
        list: List of genres associated with each track ID.
    """
    track_genres = []

    for track_id in tracks_id:
        try:
            # Obtener la información de la pista
            track_info = sp.track(track_id)             
            # Obtener los artistas asociados a la pista
            artist_id = track_info['artists'][0]['id']                        
            # Obtener la información del artista
            genres = sp.artist(artist_id)['genres']
            
            # Si hay géneros disponibles para el artista, agregar el primero a la lista de géneros de la pista
            if genres:
                track_genres.append(genres)
            else:
                track_genres.append("Unknown")

        except Exception as e:
            print(f"Error getting genres for track {track_id}: {e}")

    return track_genres

'''---------------------------------------------------------------------------------------------------------------------'''

def get_popularity(tracks_id, sp=sp):
    """
    Get the popularity score for each track ID from Spotify.

    Args:
    tracks_id (list): List of track IDs.
    sp: Authenticated Spotipy object.

    Returns:
    list: List of popularity scores associated with each track ID.
    """
    popularity = []

    for track_id in tracks_id:
        try:
            # Obtener la información de la pista
            track_info = sp.track(track_id)
            # Extraer el parámetro de popularidad
            pop = track_info.get('popularity', None)
            # Agregar la popularidad a la lista general
            popularity.append(pop)
            
        except Exception as e:
            print(f"Error getting popularity for track {track_id}: {e}")

    return popularity

'''---------------------------------------------------------------------------------------------------------------------'''

def get_features(tracks_id, sp=sp):
    """
    Get the audio features for each track ID from Spotify.

    Args:
    tracks_id (list): List of track IDs.
    sp: Authenticated Spotipy object.

    Returns:
    list: List of dictionaries containing audio features for each track ID.
          Returns None if no features are found.
    """
    features = []

    for track_id in tracks_id:
        try:
            # Obtener las características de audio de la pista
            audio_features = sp.audio_features(track_id)
            
            # Filtrar solo las características que deseas
            filtered_features = {
                'danceability': audio_features[0]['danceability'],
                'energy': audio_features[0]['energy'],
                'key': audio_features[0]['key'],
                'loudness': audio_features[0]['loudness'],
                'mode': audio_features[0]['mode'],
                'speechiness': audio_features[0]['speechiness'],
                'acousticness': audio_features[0]['acousticness'],
                'instrumentalness': audio_features[0]['instrumentalness'],
                'liveness': audio_features[0]['liveness'],
                'valence': audio_features[0]['valence'],
                'tempo': audio_features[0]['tempo'],
                'duration_ms': audio_features[0]['duration_ms'],
                'time_signature': audio_features[0]['time_signature']
            }

            # Agregar las características filtradas a la lista general
            features.append(filtered_features)
            
        except Exception as e:
            print(f"Error getting features for track {track_id}: {e}")

    return features

'''---------------------------------------------------------------------------------------------------------------------'''

def get_related_artists(tracks_id, function=get_artist_id, sp=sp):
    """
    Get a list of 20 related artists for each artist associated with the given track IDs from Spotify.

    Args:
    tracks_id (list): List of track IDs.
    function: Function to retrieve artist IDs associated with track IDs.
    sp: Authenticated Spotipy object.

    Returns:
    list: List of dictionaries containing information about related artists for each artist associated with the track IDs.
          Each dictionary contains the 'id', 'name', and 'genres' of a related artist.
          Returns None if no related artists are found for any artist.
    """
    artist_ids = function(tracks_id, sp=sp)
    if not artist_ids:
        return None
    
    related_artists = []

    for artist_id in artist_ids:
        try:
            # Obtener información sobre artistas relacionados
            related_artists_info = sp.artist_related_artists(artist_id)['artists']
            
            # Extraer la información relevante de cada artista relacionado
            rel_art = [{'id': artist['id'], 'name': artist['name'], 'genres': artist['genres']} 
                               for artist in related_artists_info]
            
            related_artists.append(rel_art)
            
        except Exception as e:
            print(f"Error getting related artists for artist {artist_id}: {e}")

    return related_artists

'''---------------------------------------------------------------------------------------------------------------------'''

