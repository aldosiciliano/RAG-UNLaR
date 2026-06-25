from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

PDF_PATH = Path("data/pdfs/prueba_pipeline.pdf")


def main() -> None:
    PDF_PATH.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(PDF_PATH), pagesize=A4)

    paginas_texto = [
        "Documento de prueba - Pagina 1.\n\n"
        "Este es un texto generico usado unicamente para validar el pipeline "
        "tecnico de extraccion, chunking, vectorizacion y recuperacion. "
        "No representa ningun caso de uso real del proyecto final.\n\n"
        "Dato de control A: el codigo de verificacion es ALFA-7731.",
        "Documento de prueba - Pagina 2.\n\n"
        "Segunda pagina con contenido distinto para comprobar que el sistema "
        "puede diferenciar entre fragmentos de distintas paginas.\n\n"
        "Dato de control B: el codigo de verificacion es BETA-4420.",
        "Documento de prueba - Pagina 3.\n\n"
        "Tercera pagina, usada para probar chunks largos con overlap. "
        "Esta pagina repite intencionalmente algunos conceptos de la pagina "
        "anterior para verificar que la busqueda por similitud distingue "
        "correctamente el contexto de cada fragmento.\n\n"
        "Dato de control C: el codigo de verificacion es GAMMA-1892.",
    ]

    for texto in paginas_texto:
        y = 800
        for linea in texto.split("\n"):
            c.drawString(50, y, linea)
            y -= 20
        c.showPage()

    c.save()
    print(f"PDF de prueba generado en {PDF_PATH}")


if __name__ == "__main__":
    main()
