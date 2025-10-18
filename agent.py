import os
import datetime
import argparse
import asyncio
from typing import List, Any

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

# ---- Konfiguracja ----
GOOGLE_MODEL = os.environ.get("GOOGLE_MODEL", "gemini-pro")
APP_NAME = os.environ.get("ADK_APP_NAME", "adk-agent-py")
USER_ID = os.environ.get("ADK_USER_ID", "user-default")
SESSION_ID = os.environ.get("ADK_SESSION_ID", "session-default")
BASE_DIR = os.path.dirname(__file__)

# ---- Narzędzia z dekoratorem @tool ----

def tell_time() -> str:
    """Zwraca aktualną datę i godzinę."""
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def create_note(text: str, filename: str) -> str:
    """Zapisuje podany tekst do pliku.

    Args:
        text: Tekst do zapisania w notatce.
        filename: Nazwa pliku, w którym ma być zapisana notatka.

    Returns:
        Komunikat potwierdzający zapisanie notatki.
    """
    notes_path = os.path.join(BASE_DIR, filename)
    os.makedirs(os.path.dirname(notes_path) or ".", exist_ok=True)
    with open(notes_path, "a", encoding="utf-8") as f:
        f.write(text.strip() + "\n")
    return f"Notatka zapisana w '{os.path.basename(notes_path)}'."

def sum_numbers(numbers: List[float]) -> float:
    """Sumuje listę podanych liczb.

    Args:
        numbers: Lista liczb do zsumowania.

    Returns:
        Suma podanych liczb.
    """
    return sum(numbers)

# ---- Główna logika agenta ADK ----

def ensure_google_api_key() -> None:
    """Sprawdza, czy klucz API Google jest ustawiony."""
    if not os.environ.get("GOOGLE_API_KEY"):
        raise RuntimeError("Brak zmiennej środowiskowej GOOGLE_API_KEY. Ustaw klucz i spróbuj ponownie.")

async def run_adk_async(instruction: str) -> str:
    """Asynchronicznie uruchamia agenta ADK z zadaną instrukcją."""
    ensure_google_api_key()

    # Definicja agenta z dostępnymi narzędziami
    agent = Agent(
        name="adk_agent",
        model=GOOGLE_MODEL,
        tools=[tell_time, create_note, sum_numbers, google_search],
        instruction="Jesteś pomocnym agentem. Wykonuj zadania, korzystając z dostępnych narzędzi. Na końcu zwróć zwięzłą odpowiedź.",
    )

    # Ustawienie sesji w pamięci
    session_service = InMemorySessionService()
    await session_service.create_session(app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID)

    # Uruchomienie agenta
    runner = Runner(agent=agent, app_name=APP_NAME, session_service=session_service)
    content = genai_types.Content(role="user", parts=[genai_types.Part(text=instruction)])
    events = runner.run_async(user_id=USER_ID, session_id=SESSION_ID, new_message=content)

    final_response = "Agent zakończył pracę, ale nie wygenerował odpowiedzi."
    async for event in events:
        if event.is_final_response():
            try:
                final_response = event.content.parts[0].text
            except (AttributeError, IndexError):
                final_response = "Otrzymano pustą odpowiedź od agenta."
            break
    
    return final_response.strip()

def run_agent(instruction: str) -> str:
    """Synchroniczna funkcja opakowująca dla `run_adk_async`."""
    return asyncio.run(run_adk_async(instruction))

# ---- Główny punkt wejścia ----

def main() -> None:
    """Przetwarza argumenty wiersza poleceń i uruchamia agenta."""
    parser = argparse.ArgumentParser(
        description="Agent oparty na Google ADK.",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog="Dostępne narzędzia: tell_time, create_note, sum_numbers, google_search."
    )
    parser.add_argument("-i", "--instruction", help="Polecenie do jednorazowego wykonania przez agenta.")
    args = parser.parse_args()

    if args.instruction:
        try:
            result = run_agent(args.instruction)
            print(result)
        except Exception as e:
            print(f"Błąd: {e}")
        return

    print("Agent Google ADK jest gotowy. Podaj polecenie lub wpisz 'exit', aby zakończyć.")
    print("Przykłady: 'Jaka jest teraz godzina?', 'Stwórz notatkę: to jest test', 'jaka jest pogoda w Warszawie?'")
    
    while True:
        try:
            user_input = input("> ").strip()
            if user_input.lower() == 'exit':
                print("Do widzenia!")
                break
            if not user_input:
                continue
            
            result = run_agent(user_input)
            print(result)

        except KeyboardInterrupt:
            print("Do widzenia!")
            break
        except Exception as e:
            print(f"Wystąpił błąd: {e}")

if __name__ == "__main__":
    main()