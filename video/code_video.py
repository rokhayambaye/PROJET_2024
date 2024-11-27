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

def create_video_with_previous_images(image_folder, output_video_path, fps=30, background_color=(0, 0, 0)):

    # Lister les fichiers PNG dans le dossier
    images = [img for img in os.listdir(image_folder) if img.endswith(".png")]
    images.sort()  # Trier les fichiers par ordre alphabétique

    # Vérifier s'il y a des images
    if not images:
        print("Aucune image PNG trouvée dans le dossier spécifié.")
        return

    # Charger la première image pour définir la taille de la vidéo
    first_image_path = os.path.join(image_folder, images[0])
    frame = cv2.imread(first_image_path, cv2.IMREAD_UNCHANGED)

    if frame is None:
        print(f"Impossible de lire la première image : {first_image_path}")
        return

    height, width = frame.shape[:2]
    size = (width, height)

    # Initialiser l'image de fond (noir par défaut)
    accumulated_image = np.full((height, width, 4), (*background_color, 255), dtype=np.uint8)

    # Initialiser le Writer vidéo
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")  # Codec pour fichier .mp4
    video = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))

    # Ajouter chaque image à la vidéo en superposant les anciennes
    for image_name in images:
        image_path = os.path.join(image_folder, image_name)
        current_image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)

        if current_image is None:
            print(f"Impossible de lire l'image : {image_path}")
            continue

        # Ajouter la nouvelle image au "fond accumulé"
        alpha = current_image[:, :, 3] / 255.0 if current_image.shape[2] == 4 else 1.0
        for c in range(0, 3):  # Pour chaque canal (B, G, R)
            accumulated_image[:, :, c] = (
                alpha * current_image[:, :, c] + (1 - alpha) * accumulated_image[:, :, c]
            ).astype(np.uint8)

        # Convertir en image RGB (supprimer la transparence)
        frame_to_write = cv2.cvtColor(accumulated_image, cv2.COLOR_BGRA2BGR)
        video.write(frame_to_write)  # Ajouter le frame à la vidéo

    # Libérer les ressources
    video.release()
    print(f"Vidéo créée avec succès : {output_video_path}")
def add_music_to_video(video_path, audio_path, output_video_with_audio_path):

    # Charger la vidéo
    video_clip = VideoFileClip(video_path)

    # Charger l'audio
    audio_clip = AudioFileClip(audio_path)

    # Répéter l'audio pour couvrir toute la durée de la vidéo
    if audio_clip.duration < video_clip.duration:
        # Calculer combien de fois répéter l'audio
        num_loops = int(video_clip.duration // audio_clip.duration) + 1
        audio_clip = concatenate_audioclips([audio_clip] * num_loops).subclip(0, video_clip.duration)

    # Ajouter l'audio à la vidéo
    video_with_audio = video_clip.set_audio(audio_clip)

    # Sauvegarder la vidéo avec la musique
    video_with_audio.write_videofile(output_video_with_audio_path, codec="libx264", audio_codec="aac")
    print(f"Vidéo avec musique créée avec succès : {output_video_with_audio_path}")



# API Key OpenRouteService
api_key = '5b3ce3597851110001cf6248669ce5ad0dd949edb915886bc923b678'
# Options de Selenium pour capturer la carte sans ouvrir de fenêtre
options = Options()
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)

# Charger les trajets depuis un fichier CSV
dft = pd.read_csv("trajets.csv", sep=',')
dftl = dft.values.tolist()

nbrSegments = 10
nbrtrajet=100 # len(dftl)
# Traitement de chaque trajet
for i in range(nbrtrajet):  # Limité les trajets 
    if dftl[i][3:5] != dftl[i][5:7]:  # Vérifier si les coordonnées sont valides
        start = (dftl[i][4], dftl[i][3])
        end = (dftl[i][6], dftl[i][5])
        trajet(dftl[i][0], driver, start, end, nbrSegments)



input_folder = "image"  # Dossier contenant les images originales
output_folder = "imaget"  # Dossier pour les images modifiées
target_color = (221, 221, 221)  # Couleur cible (blanc)
tolerance = 10  # Tolérance pour une correspondance proche

make_color_transparent(input_folder, output_folder, target_color, tolerance)

# Exemple d'utilisation
image_folder = "imaget"  # Dossier contenant les images PNG
output_video = "output_video_with_history.mp4"  # Chemin de la vidéo de sortie
fps = 5  # Images par seconde
background_color = (0, 0, 0)  # Couleur de fond initiale (noir)

create_video_with_previous_images(image_folder, output_video, fps, background_color)
# Ajouter de la musique à la vidéo créée
audio_file = "musique.mp3"  # Chemin de la musique à ajouter
output_video_with_audio = "video_with_audio_andH.mp4"  # Chemin de la vidéo de sortie avec musique
add_music_to_video(output_video, audio_file, output_video_with_audio)



# Fermer le navigateur Selenium
driver.quit()

