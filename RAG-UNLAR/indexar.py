import argparse
from pathlib import Path

from config import PDF_DIR
from modules.chunking import dividir_en_chunks
from modules.ingestion import cargar_pdfs
from modules.vectorstore import contar, indexar_chunks, limpiar


def main() -> None:
    parser = argparse.ArgumentParser(description="Indexar PDFs en ChromaDB.")
    parser.add_argument("--limpiar", action="store_true", help="Recrear colección antes de indexar.")
    args = parser.parse_args()

    PDF_DIR.mkdir(parents=True, exist_ok=True)
    if args.limpiar:
        limpiar()
        print("Colección limpiada.")

    paginas = cargar_pdfs(PDF_DIR)
    chunks = dividir_en_chunks(paginas)
    nuevos = indexar_chunks(chunks)
    pdfs = sorted({pagina["archivo"] for pagina in paginas})

    print(f"Páginas extraídas: {len(paginas)}")
    print(f"Chunks generados: {len(chunks)}")
    print(f"Chunks indexados: {nuevos}")
    print(f"Total en BD: {contar()}")
    print("PDFs indexados:")
    for pdf in pdfs:
        print(f"- {pdf}")


if __name__ == "__main__":
    main()
