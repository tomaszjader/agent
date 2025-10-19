import datetime

def tell_time() -> str:
    """Zwraca aktualną datę i godzinę."""
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")