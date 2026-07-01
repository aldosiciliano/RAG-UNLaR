from pathlib import Path

import pdfplumber
from config import PDF_URLS


def cargar_pdf(ruta_pdf: str | Path) -> list[dict]:
    ruta = Path(ruta_pdf)
    paginas: list[dict] = []

    with pdfplumber.open(ruta) as pdf:
        for idx, pagina in enumerate(pdf.pages, start=1):
            texto = pagina.extract_text() or ""
            texto = texto.strip()
            if not texto:
                continue
            paginas.append(
                {
                    "archivo": ruta.name,
                    "ruta": str(ruta),
                    "url": PDF_URLS.get(ruta.name, ""),
                    "pagina": idx,
                    "texto": texto,
                }
            )

    return paginas


def cargar_pdfs(directorio: str | Path) -> list[dict]:
    rutas = sorted(Path(directorio).glob("*.pdf"))
    paginas: list[dict] = []
    for ruta in rutas:
        paginas.extend(cargar_pdf(ruta))
    return paginas
