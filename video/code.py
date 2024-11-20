import pandas as pd 
import requests
import folium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import random
from PIL import Image
import os
import cv2
import os
import numpy as np  
from moviepy.editor import VideoFileClip, AudioFileClip
from moviepy.audio.AudioClip import concatenate_audioclips 

# Fonction pour obtenir la trajectoire à partir de l'API OpenRouteService
def fetch_route(start_coords, end_coords, api_key):
    """
    Récupere les coordonnees d'une trajectoire entre deux points en utilisant l'API OpenRouteService.

    Arguments :
    - start_coords : Tuple contenant les coordonnees de depart (latitude, longitude).
    - end_coords : Tuple contenant les coordonnees d'arrivee (latitude, longitude).
    - api_key : Cle API pour authentification.

    Retour :
    - Liste de tuples (latitude, longitude) representant la trajectoire.
    """
    url = "https://api.openrouteservice.org/v2/directions/driving-car"
    headers = {"Authorization": api_key}
    params = {
        'start': f"{start_coords[1]},{start_coords[0]}",  # Longitude, Latitude
        'end': f"{end_coords[1]},{end_coords[0]}"         # Longitude, Latitude
    }
    response = requests.get(url, headers=headers, params=params)
    route = response.json()

    if 'features' in route and len(route['features']) > 0:
        coordinates = route['features'][0]['geometry']['coordinates']
        return [(lat, lon) for lon, lat in coordinates]  # Convertir à (lat, lon)
    else:
        print("Pas de route trouvée.")
        return []
    
    # Fonction pour diviser la trajectoire en morceaux
def divide_trajectory(trajectory, num_segments):
    chunk_size = len(trajectory) // num_segments
    segments = []
    
    for i in range(num_segments):
        start_index = i * chunk_size
        end_index = (i + 1) * chunk_size if i != num_segments - 1 else len(trajectory)
        segments.append(trajectory[start_index:end_index])
    
    return segments
# Fonction principale pour générer des images de trajectoires
def trajet(idt, driver, start_coords, end_coords, num_segments):
    """
    Génère des images pour les segments d'une trajectoire et les enregistre.

    Arguments :
    - idt : Identifiant du trajet.
    - driver : Instance Selenium WebDriver pour capturer les cartes.
    - start_coords : Coordonnées de départ (latitude, longitude).
    - end_coords : Coordonnées de fin (latitude, longitude).
    - num_segments : Nombre de segments pour diviser la trajectoire.

    """
    # Obtenir la trajectoire complète
    trajectory = fetch_route(start_coords, end_coords, api_key)

    # Diviser la trajectoire en segments
    segments = divide_trajectory(trajectory, num_segments)

    # Créer un répertoire pour les images si nécessaire
    if not os.path.exists("image"):
        os.makedirs("image")

    # Créer et sauvegarder les images pour chaque segment
    for idx, segment in enumerate(segments):
        # Créer une carte pour le segment actuel
        m = folium.Map(
            location=start_coords,
            tiles="Stamen Toner",
            zoom_start=14,
            attr="OpenStreetMap"
        )    
        # Ajouter la ligne représentant le segment
        folium.PolyLine(segment, color="#FFFFFF", weight=5, opacity=0.7).add_to(m)

        # Sauvegarder la carte temporairement
        map_html = f"segment_map_{idt}_{idx}.html"
        m.save(map_html)

        # Capturer une capture d'écran via Selenium
        driver.get(f"file://{os.path.abspath(map_html)}")
        time.sleep(2)  # Attendre le chargement complet
        screenshot_path = f"image/{idt}_{idx}.png"
        driver.save_screenshot(screenshot_path)
        
        # Supprimer le fichier HTML temporaire
        os.remove(map_html)

# Fonction pour rendre une couleur d'image transparente
def make_color_transparent(input_folder, output_folder, target_color, tolerance=0):
       # Créer le dossier de sortie s'il n'existe pas
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Parcourir les fichiers dans le dossier d'entrée
    for filename in os.listdir(input_folder):
        if filename.endswith(".png") or filename.endswith(".jpg"):  # Gérer PNG et JPG
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)

            try:
                # Ouvrir l'image
                image = Image.open(input_path).convert("RGBA")
                datas = image.getdata()

                # Préparer une nouvelle liste de pixels
                new_data = []
                for item in datas:
                    r, g, b, a = item  # Couleur actuelle
                    if abs(r - target_color[0]) <= tolerance and \
                       abs(g - target_color[1]) <= tolerance and \
                       abs(b - target_color[2]) <= tolerance:
                        # Rendre ce pixel transparent
                        new_data.append((r, g, b, 0))
                    else:
                        new_data.append((r, g, b, a))

                # Appliquer les modifications
                image.putdata(new_data)
                # Enregistrer l'image modifiée
                image.save(output_path, "PNG")

            except Exception as e:
                print(f"Erreur lors du traitement de l'image {filename} : {e}")