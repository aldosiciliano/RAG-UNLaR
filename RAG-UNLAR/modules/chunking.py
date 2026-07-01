from config import CHUNK_OVERLAP, CHUNK_SIZE


def _partir_texto(texto: str, chunk_size: int, overlap: int) -> list[str]:
    texto = " ".join(texto.split())
    if not texto:
        return []

    chunks: list[str] = []
    inicio = 0
    while inicio < len(texto):
        fin = min(inicio + chunk_size, len(texto))
        corte = fin

        if fin < len(texto):
            ultimo_punto = texto.rfind(". ", inicio, fin)
            if ultimo_punto > inicio + chunk_size // 2:
                corte = ultimo_punto + 1

        chunks.append(texto[inicio:corte].strip())
        if corte >= len(texto):
            break
        inicio = max(corte - overlap, 0)

    return [chunk for chunk in chunks if chunk]


def dividir_en_chunks(
    paginas: list[dict],
    chunk_size: int = CHUNK_SIZE,
    overlap: int = CHUNK_OVERLAP,
) -> list[dict]:
    chunks: list[dict] = []

    for pagina in paginas:
        partes = _partir_texto(pagina["texto"], chunk_size, overlap)
        for idx, texto in enumerate(partes):
            chunks.append(
                {
                    "id": f"{pagina['archivo']}::p{pagina['pagina']}::c{idx}",
                    "archivo": pagina["archivo"],
                    "ruta": pagina["ruta"],
                    "url": pagina.get("url", ""),
                    "pagina": pagina["pagina"],
                    "chunk": idx,
                    "texto": texto,
                }
            )

    return chunks
