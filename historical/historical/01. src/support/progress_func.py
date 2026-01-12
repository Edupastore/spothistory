import pickle


def save_progress(all_data, processed_track_ids, filename='progress.pkl'):
    """
    Save the progress of data extraction to a pickle file.

    Args:
        all_data (dict): A dictionary containing the extracted data up to the current point.
        processed_track_ids (list): A list of track identifiers that have been processed.
        filename (str, optional): The name of the file to save the progress to. Defaults to 'progress.pkl'.

    Returns:
        None
    """
    with open(filename, 'wb') as f:
        pickle.dump((all_data, processed_track_ids), f)
        
        
def load_progress(filename='progress.pkl'):
    """
    Load the progress of data extraction from a pickle file.

    Args:
        filename (str, optional): The name of the file containing the saved progress. Defaults to 'progress.pkl'.

    Returns:
        tuple: A tuple containing two elements:
            - A dictionary containing the loaded data extracted up to the previous point.
            - A list of track identifiers that have been processed.
    """
    try:
        with open(filename, 'rb') as f:
            return pickle.load(f)
    except FileNotFoundError:
        return {}, []
    
    
def read_progress(file_path):
    """
    Lee y carga el contenido de un archivo de progreso guardado previamente.

    Args:
        file_path (str): La ruta del archivo de progreso a leer.

    Returns:
        content (object): El contenido del archivo de progreso cargado en memoria.
    """
    with open(file_path, 'rb') as f:
        content = pickle.load(f)
    return content