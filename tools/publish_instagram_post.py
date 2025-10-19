import os
from instagrapi import Client

def publish_post(photo_path: str, caption: str) -> str:
    """Publikuje post na Instagramie ze wskazanym zdjęciem i opisem."""
    username = os.environ.get("INSTAGRAM_USERNAME")
    password = os.environ.get("INSTAGRAM_PASSWORD")

    if not all([username, password]):
        return "Brak danych logowania do Instagrama. Ustaw zmienne środowiskowe."

    client = Client()
    try:
        client.login(username, password)
        client.photo_upload(photo_path, caption)
        return "Post został opublikowany pomyślnie!"
    except Exception as e:
        return f"Wystąpił błąd podczas publikacji: {e}"