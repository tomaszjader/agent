def create_note(title: str, text: str) -> str:
    """Tworzy notatkę i zapisuje ją do pliku lokalnego.

    Args:
        title: Tytuł notatki (używany jako nazwa pliku).
        text: Treść notatki.

    Returns:
        Komunikat potwierdzający zapisanie notatki.
    """
    try:
        with open(title, "w", encoding="utf-8") as f:
            f.write(text)
        return f"Notatka została zapisana w pliku '{title}'."
    except Exception as e:
        return f"Wystąpił błąd podczas zapisywania notatki: {e}"