import gkeepapi
import os

def create_google_keep_note(title, text):
    email = os.environ.get("GOOGLE_KEEP_EMAIL")
    master_token = os.environ.get("GOOGLE_KEEP_MASTER_TOKEN")

    if not email or not master_token:
        return "Brak adresu e-mail lub tokena master do Google Keep w zmiennych środowiskowych."

    keep = gkeepapi.Keep()
    try:
        keep.authenticate(email, master_token)
        note = keep.createNote(title, text)
        keep.sync()
        return f"Notatka '{title}' została pomyślnie utworzona w Google Keep."
    except gkeepapi.exception.LoginException as e:
        return f"Błąd logowania: {e}"