from config import TOP_K
from modules.vectorstore import buscar_en_store


def buscar(consulta: str, k: int = TOP_K) -> list[dict]:
    return buscar_en_store(consulta, n_resultados=k)
