# Agent oparty na Google ADK

Prosty, konfigurowalny agent AI zbudowany w całości przy użyciu biblioteki `google-adk`. Agent potrafi korzystać z zdefiniowanych narzędzi, aby odpowiadać na pytania i wykonywać zadania w języku naturalnym.

## Główne cechy

- **Architektura oparta na Google ADK**: Wykorzystuje oficjalną bibliotekę `google-adk` do planowania, zarządzania sesją i wywoływania narzędzi.
- **Narzędzia**: Agent ma dostęp do następujących narzędzi:
  - `tell_time`: Podaje aktualną datę i godzinę.
  - `create_note`: Tworzy notatki na komputerze.
  - `sum_numbers`: Sumuje listę liczb.
  - `google_search`: Wyszukuje informacje w internecie (wbudowane narzędzie ADK).
  - `propose_caption`: Proponuje opis do posta na Instagramie.
  - `publish_post`: Publikuje post na Instagramie.
- **Model Gemini**: Działa w oparciu o modele z rodziny Google Gemini (np. `gemini-2.5-flash`).
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
    Możesz zmienić domyślny model `gemini-2.5-flash` na inny kompatybilny model z rodziny Gemini. Możesz również dostosować identyfikatory sesji, jeśli jest to potrzebne.

## Uruchomienie

Agenta można uruchomić na dwa sposoby:

### 1. Tryb interaktywny (w konsoli)

Uruchom skrypt `agent.py` bez żadnych argumentów, aby rozpocząć rozmowę z agentem w terminalu. Wpisz `exit`, aby zakończyć.

```bash
python agent.py
```

**Przykład:**
```
> Jaka jest teraz godzina?
2023-10-27 10:30:00

> Stwórz notatkę o nazwie 'lista.txt' z tekstem: kupić mleko
Notatka została zapisana w pliku 'lista.txt'.

> Jaka jest stolica Francji?
Stolicą Francji jest Paryż.
```

### 2. Tryb jednorazowy (w konsoli)

Użyj flagi `-i` lub `--instruction`, aby przekazać pojedyncze polecenie do skryptu `agent.py`. Agent wykona zadanie i zakończy działanie.

```bash
python agent.py --instruction "Zsumuj liczby 10, 25 i 7.5"
```

**Odpowiedź:**
```
Suma: 42.5
```

### 3. Bot na Telegramie

Agent może być również uruchomiony jako bot na Telegramie, co pozwala na interakcję z nim za pomocą wiadomości.

**Konfiguracja Bota na Telegramie:**

1.  **Utwórz bota i uzyskaj token:**
    -   Porozmawiaj z [@BotFather](https://t.me/BotFather) na Telegramie.
    -   Użyj komendy `/newbot`, aby stworzyć nowego bota.
    -   Postępuj zgodnie z instrukcjami, a na końcu otrzymasz token.

2.  **Dodaj token do pliku `.env`:**
    Otwórz plik `.env` i dodaj nową zmienną `TELEGRAM_BOT_TOKEN`:
    ```env
    GOOGLE_API_KEY="TwojKluczApiGoogle"
    TELEGRAM_BOT_TOKEN="TwojTokenBotaTelegrama"
    ```

**Uruchomienie Bota:**

Aby uruchomić bota, wykonaj poniższą komendę:

```bash
python bot.py
```

Bot będzie działał w tle i odpowiadał na wiadomości wysyłane na Telegramie. Możesz wysyłać do niego zarówno polecenia tekstowe, jak i zdjęcia.

## Struktura projektu

```
agent/
│
├── .env.example      # Przykład konfiguracji zmiennych środowiskowych
├── .gitignore        # Pliki ignorowane przez Git
├── agent.py          # Główny skrypt agenta (tryb konsolowy)
├── bot.py            # Skrypt do uruchomienia bota na Telegramie
├── requirements.txt  # Zależności projektu
├── README.md         # Ten plik
│
└───tools/            # Katalog z narzędziami
    ├── __init__.py
    ├── create_google_keep_note.py
    ├── create_note.py
    ├── prepare_instagram_post.py
    ├── publish_instagram_post.py
    ├── sum_numbers.py
    └── tell_time.py
```