from __future__ import annotations

import hashlib

import chromadb
from sentence_transformers import SentenceTransformer

from config import COLLECTION_NAME, DB_DIR, EMBEDDING_MODEL

_modelo: SentenceTransformer | None = None


def _cliente() -> chromadb.PersistentClient:
    DB_DIR.mkdir(parents=True, exist_ok=True)
    return chromadb.PersistentClient(path=str(DB_DIR))


def _coleccion():
    return _cliente().get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )


def _embedding_model() -> SentenceTransformer:
    global _modelo
    if _modelo is None:
        _modelo = SentenceTransformer(EMBEDDING_MODEL)
    return _modelo


def _ids_existentes(ids: list[str]) -> set[str]:
    if not ids:
        return set()
    resultado = _coleccion().get(ids=ids, include=[])
    return set(resultado.get("ids", []))


def _id_estable(chunk: dict) -> str:
    base = f"{chunk['archivo']}|{chunk['pagina']}|{chunk['chunk']}|{chunk['texto']}"
    digest = hashlib.sha1(base.encode("utf-8")).hexdigest()
    return f"{chunk['archivo']}:{chunk['pagina']}:{chunk['chunk']}:{digest[:12]}"


def embedding_textos(textos: list[str]) -> list[list[float]]:
    embeddings = _embedding_model().encode(textos, normalize_embeddings=True)
    return embeddings.tolist()


def indexar_chunks(chunks: list[dict]) -> int:
    if not chunks:
        return 0

    ids = [_id_estable(chunk) for chunk in chunks]
    existentes = _ids_existentes(ids)
    nuevos = [(id_, chunk) for id_, chunk in zip(ids, chunks) if id_ not in existentes]

    if not nuevos:
        return 0

    textos = [chunk["texto"] for _, chunk in nuevos]
    metadatas = [
        {
            "archivo": chunk["archivo"],
            "ruta": chunk["ruta"],
            "pagina": chunk["pagina"],
            "chunk": chunk["chunk"],
        }
        for _, chunk in nuevos
    ]
    embeddings = embedding_textos(textos)

    _coleccion().add(
        ids=[id_ for id_, _ in nuevos],
        documents=textos,
        metadatas=metadatas,
        embeddings=embeddings,
    )
    return len(nuevos)


def buscar_en_store(consulta: str, n_resultados: int) -> list[dict]:
    consulta_embedding = embedding_textos([consulta])[0]
    resultado = _coleccion().query(
        query_embeddings=[consulta_embedding],
        n_results=n_resultados,
        include=["documents", "metadatas", "distances"],
    )

    documentos = resultado.get("documents", [[]])[0]
    metadatas = resultado.get("metadatas", [[]])[0]
    distancias = resultado.get("distances", [[]])[0]

    filas: list[dict] = []
    for texto, metadata, distancia in zip(documentos, metadatas, distancias):
        filas.append(
            {
                "texto": texto,
                "archivo": metadata["archivo"],
                "ruta": metadata["ruta"],
                "pagina": metadata["pagina"],
                "chunk": metadata["chunk"],
                "similitud": 1 - float(distancia),
            }
        )
    return filas


def contar() -> int:
    return _coleccion().count()


def limpiar() -> None:
    cliente = _cliente()
    try:
        cliente.delete_collection(COLLECTION_NAME)
    except Exception:
        pass
    cliente.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )
