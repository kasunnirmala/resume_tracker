from sentence_transformers import SentenceTransformer


def text_embeddings(text: str) -> list[float]:
    model = SentenceTransformer("all-MiniLM-L6-v2")
    return model.encode(text).tolist()
