def chunk_text(text, chunk_size=500):
    """Splits text into chunks of a given size."""
    return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]
