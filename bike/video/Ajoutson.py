from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_audioclips

def add_music_to_video(video_path, audio_path, output_video_with_audio_path, duration):
    """
    Ajoute une piste audio à une vidéo et ajuste leur durée.
    Paramètres :
    -----------
    video_path : str
        Chemin vers le fichier vidéo d'entrée.
    audio_path : str
        Chemin vers le fichier audio d'entrée.
    output_video_with_audio_path : str
        Chemin pour enregistrer la vidéo de sortie avec l'audio ajouté.
    duration : int ou float
        Durée souhaitée pour la vidéo et l'audio (en secondes).

    Sortie :
    --------
    None
        La vidéo avec l'audio est enregistrée à l'emplacement spécifié.

    Exemple d'utilisation :
    -----------------------
    add_music_to_video(
        "docs/Video/bike_animation_12_Mai.mp4",
        "bike/video/musique.mp3",
        "docs/Video/bike_animation_12_Mai_son.mp4",
        57
    )
    """
    import os
    if not os.path.isfile(video_path):
        print(f"Erreur : La vidéo '{video_path}' est introuvable.")
        return
    if not os.path.isfile(audio_path):
        print(f"Erreur : L'audio '{audio_path}' est introuvable.")
        return

    try:
        # Charger la vidéo et couper à la durée souhaitée
        video_clip = VideoFileClip(video_path).subclip(0, duration)

        # Charger l'audio
        audio_clip = AudioFileClip(audio_path)

        # Ajuster la durée de l'audio à la durée souhaitée
        if audio_clip.duration > duration:
            # Couper l'audio à la durée
            audio_clip = audio_clip.subclip(0, duration)
        elif audio_clip.duration < duration:
            # Répéter l'audio si nécessaire
            num_loops = int(duration // audio_clip.duration) + 1
            audio_clip = concatenate_audioclips([audio_clip] * num_loops).subclip(0, duration)

        # Ajouter l'audio à la vidéo
        video_with_audio = video_clip.set_audio(audio_clip)

        # Sauvegarder la vidéo avec la musique
        video_with_audio.write_videofile(output_video_with_audio_path, codec="libx264", audio_codec="aac")
        print(f"Vidéo avec musique créée avec succès : {output_video_with_audio_path}")

    except Exception as e:
        print(f"Erreur inattendue : {e}")

# Ajouter la musique à la vidéo du 12 Mai
add_music_to_video("docs/Video/bike_animation_12_Mai.mp4", "bike/video/musique.mp3", "docs/Video/bike_animation_12_Mai_son.mp4", 57)

# Ajouter la musique à la vidéo du 14 Mai
add_music_to_video("docs/Video/bike_animation_14_Mai.mp4", "bike/video/musique.mp3", "docs/Video/bike_animation_14_Mai_son.mp4", 57)
