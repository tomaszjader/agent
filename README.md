# Agent oparty na Google ADK

Prosty, konfigurowalny agent AI zbudowany w całości przy użyciu biblioteki `google-adk`. Agent potrafi korzystać z zdefiniowanych narzędzi, aby odpowiadać na pytania i wykonywać zadania w języku naturalnym.

## Główne cechy

- **Architektura oparta na Google ADK**: Wykorzystuje oficjalną bibliotekę `google-adk` do planowania, zarządzania sesją i wywoływania narzędzi.
- **Narzędzia**: Agent ma dostęp do następujących narzędzi:
  - `tell_time`: Podaje aktualną datę i godzinę.
  - `create_note`: Tworzy i zapisuje notatki tekstowe do plików.
  - `sum_numbers`: Sumuje listę liczb.
  - `google_search`: Wyszukuje informacje w internecie (wbudowane narzędzie ADK).
- **Model Gemini**: Działa w oparciu o modele z rodziny Google Gemini (np. `gemini-1.5-flash`).
- **Tryb interaktywny i jednorazowy**: Można go uruchomić w pętli do prowadzenia rozmowy lub do wykonania pojedynczej instrukcji.

## Wymagania

- Python 3.9+
- Klucz API od Google (Google AI Studio)

## Instalacja

1.  **Sklonuj repozytorium lub pobierz pliki.**

2.  **Utwórz i aktywuj wirtualne środowisko (zalecane):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # Na Windows: venv\Scripts\activate
    ```

3.  **Zainstaluj zależności:**
    ```bash
    python -m pip install -r requirements.txt
    ```

## Konfiguracja

1.  **Skopiuj plik `.env.example` do nowego pliku o nazwie `.env`:**
    ```bash
    cp .env.example .env
    ```

2.  **Otwórz plik `.env` i wklej swój klucz API od Google:**
    ```env
    GOOGLE_API_KEY="TwojKluczApiGoogle"
    ```

3.  **(Opcjonalnie) Zmień model Gemini lub identyfikatory sesji:**
    Możesz zmienić domyślny model `gemini-1.5-flash` na inny kompatybilny model z rodziny Gemini. Możesz również dostosować identyfikatory sesji, jeśli jest to potrzebne.

## Uruchomienie

Agenta można uruchomić na dwa sposoby:

### 1. Tryb interaktywny

Uruchom skrypt bez żadnych argumentów, aby rozpocząć rozmowę z agentem. Wpisz `exit`, aby zakończyć.

```bash
python agent.py
```

**Przykład:**
```
> Jaka jest teraz godzina?
2023-10-27 10:30:00

> Stwórz notatkę o nazwie 'lista.txt' z tekstem: kupić mleko
Notatka zapisana w 'lista.txt'.

> Jaka jest stolica Francji?
Stolicą Francji jest Paryż.
```

### 2. Tryb jednorazowy

Użyj flagi `-i` lub `--instruction`, aby przekazać pojedyncze polecenie. Agent wykona zadanie i zakończy działanie.

```bash
python agent.py --instruction "Zsumuj liczby 10, 25 i 7.5"
```

**Odpowiedź:**
```
Suma: 42.5
```

## Struktura projektu

- `agent.py`: Główny plik zawierający całą logikę agenta, definicje narzędzi i pętlę uruchomieniową.
- `requirements.txt`: Lista zależności Pythona (`google-adk`, `python-dotenv` itp.).
- `.env.example`: Szablon pliku konfiguracyjnego dla kluczy API.
- `README.md`: Ten plik.