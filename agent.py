import os
import asyncio

try:
    from dotenv import load_dotenv, find_dotenv
    load_dotenv(find_dotenv())
except ImportError:
    pass

from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.tools import google_search
from google.genai import types as genai_types

from tools.tell_time import tell_time
from tools.create_note import create_note
from tools.sum_numbers import sum_numbers
from tools.prepare_instagram_post import propose_caption
from tools.publish_instagram_post import publish_post

# ---- Konfiguracja ----
GOOGLE_MODEL = os.environ.get("GOOGLE_MODEL", "gemini-pro")
APP_NAME = os.environ.get("ADK_APP_NAME", "adk-agent-py")
BASE_DIR = os.path.dirname(__file__)

# ---- Globalne instancje ----
session_service = InMemorySessionService()
created_sessions = set()

agent = Agent(
    name="adk_agent",
    model=GOOGLE_MODEL,
    tools=[tell_time, create_note, sum_numbers, google_search, propose_caption, publish_post],
    instruction="""🧠 Agent Tomek — Twój asystent do postów i zadań

Opis:
Jesteś agentem Tomkiem, którego zadaniem jest pomaganie użytkownikowi w:

tworzeniu i publikowaniu postów na Instagramie,

sumowaniu liczb,

wyszukiwaniu informacji w internecie,

tworzeniu notatek w Google Keep,

oraz udzielaniu informacji o czasie.

Twoim głównym celem jest wsparcie użytkownika w przygotowaniu i publikacji posta na Instagramie.



🪜 Procedura publikacji posta

Propozycja opisu:
Użyj narzędzia propose_caption, aby wygenerować propozycję opisu posta.

Akceptacja lub edycja:
Zapytaj użytkownika, czy akceptuje zaproponowany opis.

Jeśli chce wprowadzić zmiany, przeanalizuj jego uwagi i wygeneruj nową propozycję.

Oczekiwanie na zdjęcie:
Po zaakceptowaniu ostatecznego opisu poproś użytkownika o przesłanie zdjęcia.
Poinformuj go, że czekasz na plik.

Potwierdzenie publikacji:
Po otrzymaniu zdjęcia (z podaną ścieżką pliku) przedstaw podsumowanie:

treść opisu,

informację o załączonym zdjęciu.
Zapytaj użytkownika o ostateczne potwierdzenie publikacji.

Publikacja:
Dopiero po otrzymaniu potwierdzenia użyj narzędzia publish_post,
przekazując ścieżkę do zdjęcia i zatwierdzony opis.

Anulowanie:
Jeśli użytkownik w dowolnym momencie zrezygnuje — anuluj proces.

🔧 Dodatkowe funkcje

Wyszukiwanie w internecie: jeśli użytkownik poprosi o znalezienie informacji — użyj google_search.

Tworzenie notatek w Google Keep: jeśli użytkownik poprosi o stworzenie notatki — użyj create_note. Pamiętaj, aby poprosić o tytuł i treść notatki.

Podawanie czasu: jeśli użytkownik zapyta o aktualny czas — użyj tell_time.

Sumowanie liczb: jeśli użytkownik poprosi o obliczenia — wykonaj odpowiednie działania matematyczne.
"""
)
runner = Runner(agent=agent, app_name=APP_NAME, session_service=session_service)

# ---- Główna logika agenta ADK ----

def ensure_google_api_key() -> None:
    """Sprawdza, czy klucz API Google jest ustawiony."""
    if not os.environ.get("GOOGLE_API_KEY"):
        raise RuntimeError("Brak zmiennej środowiskowej GOOGLE_API_KEY. Ustaw klucz i spróbuj ponownie.")

async def run_adk_async(session_id: str, instruction: str) -> str:
    """Asynchronicznie uruchamia agenta ADK z zadaną instrukcją."""
    ensure_google_api_key()

    # Użycie globalnych instancji i ręczne zarządzanie sesją
    if session_id not in created_sessions:
        await session_service.create_session(app_name=APP_NAME, user_id="user-default", session_id=session_id)
        created_sessions.add(session_id)

    content = genai_types.Content(role="user", parts=[genai_types.Part(text=instruction)])
    events = runner.run_async(user_id="user-default", session_id=session_id, new_message=content)

    final_response = "Agent zakończył pracę, ale nie wygenerował odpowiedzi."
    async for event in events:
        if event.is_final_response():
            try:
                final_response = event.content.parts[0].text
            except (AttributeError, IndexError):
                final_response = "Otrzymano pustą odpowiedź od agenta."
            break
    
    return final_response.strip()