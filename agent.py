import os
import json
import datetime
from typing import Any, Dict, List

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

import argparse


# ---- Akcje ----

def action_tell_time() -> str:
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def action_create_note(text: str, filename: str = "notes.txt") -> str:
    base_dir = os.path.dirname(__file__)
    notes_path = os.path.join(base_dir, filename or "notes.txt")
    os.makedirs(os.path.dirname(notes_path), exist_ok=True)
    with open(notes_path, "a", encoding="utf-8") as f:
        f.write(text.strip() + "\n")
    return f"Notatka zapisana w '{os.path.basename(notes_path)}'."


def action_sum_numbers(numbers: List[Any]) -> float:
    cleaned: List[float] = []
    for n in numbers:
        try:
            cleaned.append(float(n))
        except Exception:
            raise ValueError(f"Nieprawidłowa liczba: {n}")
    return sum(cleaned)


# ---- Wybór akcji przez LLM ----

def choose_action_via_llm(instruction: str) -> Dict[str, Any]:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "Brak zmiennej środowiskowej OPENAI_API_KEY. Ustaw klucz i spróbuj ponownie."
        )

    if OpenAI is None:
        raise RuntimeError(
            "Brak biblioteki 'openai'. Zainstaluj: python -m pip install openai"
        )

    client = OpenAI(api_key=api_key)

    system_prompt = (
        "Jesteś agentem, który wybiera i wykonuje jedną akcję z listy.\n"
        "Dostępne akcje i ich argumenty:\n"
        "- tell_time: nie przyjmuje argumentów.\n"
        "- create_note: args={\"text\": string, \"filename\": string (opcjonalny)}.\n"
        "- sum_numbers: args={\"numbers\": array[number]}.\n\n"
        "Zwróć WYŁĄCZNIE poprawny JSON w formacie:\n"
        "{\n  \"action\": \"<tell_time|create_note|sum_numbers>\",\n  \"args\": { ... }\n}\n"
        "Bez komentarzy, bez dodatkowego tekstu.\n"
        "Jeśli polecenie nie pasuje idealnie, wybierz najbardziej sensowną akcję."
    )

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": instruction},
        ],
        response_format={"type": "json_object"},
        temperature=0,
    )

    content = completion.choices[0].message.content
    try:
        parsed = json.loads(content)
    except json.JSONDecodeError as e:
        raise RuntimeError(f"Nie udało się sparsować JSON-a z modelu: {e}\nOtrzymano: {content}")

    if "action" not in parsed:
        raise RuntimeError(f"Brak klucza 'action' w odpowiedzi: {parsed}")
    if "args" not in parsed:
        parsed["args"] = {}

    return parsed


# ---- Wykonanie akcji lokalnie ----

def execute_action(action_name: str, args: Dict[str, Any]) -> str:
    if action_name == "tell_time":
        return action_tell_time()

    if action_name == "create_note":
        text = str(args.get("text", "")).strip()
        if not text:
            raise ValueError("'create_note' wymaga argumentu 'text'.")
        filename = str(args.get("filename", "notes.txt")).strip() or "notes.txt"
        return action_create_note(text=text, filename=filename)

    if action_name == "sum_numbers":
        numbers = args.get("numbers")
        if not isinstance(numbers, list) or not numbers:
            raise ValueError("'sum_numbers' wymaga listy 'numbers'.")
        result = action_sum_numbers(numbers)
        return f"Suma: {result}"

    raise ValueError(f"Nieznana akcja: {action_name}")


def run_agent(instruction: str) -> str:
    decision = choose_action_via_llm(instruction)
    action_name = decision["action"]
    args = decision.get("args", {})
    return execute_action(action_name, args)


def main() -> None:
    parser = argparse.ArgumentParser(description="Prosty agent (akcje: tell_time, create_note, sum_numbers)")
    parser.add_argument("-i", "--instruction", help="Polecenie w języku naturalnym do jednorazowego uruchomienia")
    args = parser.parse_args()

    if args.instruction:
        try:
            result = run_agent(args.instruction)
            print(result)
        except Exception as e:
            print(f"Błąd: {e}")
        return

    print("Prosty agent (akcje: tell_time, create_note, sum_numbers)")
    print("Podaj polecenie (np. 'Dodaj 2 i 5', 'Zapisz notatkę: ...', 'Jaka jest teraz godzina?')")
    try:
        user_input = input("> ").strip()
    except KeyboardInterrupt:
        print("\nPrzerwano.")
        return

    if not user_input:
        print("Brak polecenia.")
        return

    try:
        result = run_agent(user_input)
        print(result)
    except Exception as e:
        print(f"Błąd: {e}")


if __name__ == "__main__":
    main()