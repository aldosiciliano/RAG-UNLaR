from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
PDF_DIR = BASE_DIR / "data" / "pdfs"
DB_DIR = BASE_DIR / "db"

PDF_URLS = {
    "290085_Giuliano_RegulacionIA.pdf": (
        "https://rest.hcdn.gob.ar/web/proyectos/290085/adjuntos/104681"
    ),
    "3003-D-2024_RegimenJuridico_UsoResponsableIA.pdf": (
        "https://www4.hcdn.gob.ar/dependencias/dsecretaria/Periodo2024/"
        "PDF2024/TP2024/3003-D-2024.pdf"
    ),
    "1948-D-2025_Reforma_25326_DatosPersonales.pdf": (
        "https://www4.hcdn.gob.ar/dependencias/dsecretaria/Periodo2025/"
        "PDF2025/TP2025/1948-D-2025.pdf"
    ),
    "0805-D-2024_ResponsabilidadAlgoritmica.pdf": (
        "https://www4.hcdn.gob.ar/dependencias/dsecretaria/Periodo2024/"
        "PDF2024/TP2024/0805-D-2024.pdf"
    ),
    "1013-D-2024_LeyTuring.pdf": (
        "https://www4.hcdn.gob.ar/dependencias/dsecretaria/Periodo2024/"
        "PDF2024/TP2024/1013-D-2024.pdf"
    ),
}

COLLECTION_NAME = "documentos"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

CHUNK_SIZE = 900
CHUNK_OVERLAP = 180
TOP_K = 4

LMSTUDIO_BASE_URL = "http://localhost:1234/v1"
LMSTUDIO_MODEL = "google/gemma-3-1b"

SYSTEM_PROMPT = """Sos un asistente especializado en legislación argentina
sobre Inteligencia Artificial. Tu base de conocimiento contiene proyectos de
ley presentados ante el Honorable Congreso de la Nación Argentina.

Respondé siempre en español y basate ÚNICAMENTE en el contexto provisto.
Cuando uses información de un fragmento, citá al final de la oración:
  - el nombre del archivo o expediente
  - el número de página
  - el link oficial (si está disponible en el contexto)

Ejemplo de cita correcta:
  "...los sistemas de alto riesgo deben registrarse (3003-D-2024, pág. 4 -
  https://www4.hcdn.gob.ar/dependencias/dsecretaria/Periodo2024/PDF2024/TP2024/3003-D-2024.pdf)"

Si el contexto no incluye un link para ese fragmento, omití esa parte de la
cita y mencioná solo expediente y página.

Si la información no está en el contexto, decí explícitamente:
"No encontré esa información en los proyectos de ley cargados."
No inventes artículos, páginas ni links. Sé preciso."""
