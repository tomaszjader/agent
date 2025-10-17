# Prosty agent z predefiniowanymi akcjami (OpenAI)

Ten prosty agent przyjmuje polecenie w języku naturalnym i, korzystając z API OpenAI, wybiera i wykonuje jedną z kilku z góry zdefiniowanych akcji.

## Dostępne akcje
- `tell_time` – zwraca aktualną lokalną datę i godzinę.
- `create_note` – zapisuje podaną treść do pliku `notes.txt` (dopisywanie na końcu).
- `sum_numbers` – sumuje liczby podane w poleceniu.

## Wymagania
- Python 3.9+
- Konto OpenAI i klucz API zapisany w zmiennej środowiskowej `OPENAI_API_KEY`

## Instalacja
1. (Opcjonalnie) utwórz i aktywuj wirtualne środowisko:
   - Windows (PowerShell):
     ```powershell
     python -m venv .venv
     .\.venv\Scripts\Activate.ps1
     ```
2. Zainstaluj zależność:
   ```powershell
   python -m pip install -r requirements.txt
   ```

## Konfiguracja klucza API
Ustaw zmienną środowiskową `OPENAI_API_KEY`:
- Windows (PowerShell):
  ```powershell
  setx OPENAI_API_KEY "twoj_klucz_api"
  # Zamknij i otwórz nowe okno terminala, aby zmiana zadziałała
  ```

Alternatywnie możesz uruchomić sesję z tymczasową zmienną:
```powershell
$env:OPENAI_API_KEY = "twoj_klucz_api"
```

## Uruchomienie
```powershell
python agent.py
```
Wpisz polecenie w języku polskim, np.:
- "Jaka jest teraz godzina?"
- "Dodaj 2 i 5"
- "Zapisz notatkę: kupić mleko i chleb"

## Jak to działa
- Skrypt wysyła Twoje polecenie do modelu z prośbą o zwrócenie czystego JSON-a wskazującego akcję (`action`) i argumenty (`args`).
- Następnie lokalnie wykonuje wybraną akcję i wyświetla wynik.
- Agent jest ograniczony tylko do zdefiniowanych akcji – nie wykonuje dowolnego kodu.

## Pliki
- `agent.py` – główny skrypt agenta
- `requirements.txt` – zależności Pythona
- `notes.txt` – (tworzony automatycznie przy pierwszym zapisie notatki)