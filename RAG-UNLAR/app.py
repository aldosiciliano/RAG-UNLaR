from pathlib import Path

import streamlit as st
from config import PDF_DIR
from modules.chunking import dividir_en_chunks
from modules.ingestion import cargar_pdfs
from modules.llm import lmstudio_disponible, preguntar
from modules.retrieval import buscar
from modules.vectorstore import contar, indexar_chunks, limpiar

try:
    from modules.llm import preguntar_stream
except ImportError:
    preguntar_stream = None


PREGUNTAS_SUGERIDAS = [
    "¿Qué propone el proyecto de Giuliano sobre clasificación de riesgo?",
    "¿Cómo define la Ley Turing el impacto de la IA en el sistema legal?",
    "¿Qué sanciones prevé el régimen de uso responsable de la IA?",
]


def _inicializar_estado() -> None:
    st.session_state.setdefault("mensajes", [])
    st.session_state.setdefault("fuentes", [])
    st.session_state.setdefault("ultima_indexacion", "")


def _listar_pdfs() -> list[Path]:
    return sorted(PDF_DIR.glob("*.pdf")) if PDF_DIR.exists() else []


def _guardar_uploads(archivos) -> list[str]:
    PDF_DIR.mkdir(parents=True, exist_ok=True)
    guardados: list[str] = []

    for archivo in archivos:
        nombre = Path(archivo.name).name
        destino = PDF_DIR / nombre
        destino.write_bytes(archivo.getbuffer())
        guardados.append(nombre)

    return guardados


def _indexar_documentos() -> tuple[int, int, int]:
    paginas = cargar_pdfs(PDF_DIR)
    chunks = dividir_en_chunks(paginas)
    nuevos = indexar_chunks(chunks)
    return len(paginas), len(chunks), nuevos


def _historial_para_llm() -> list[dict]:
    return [
        {"role": mensaje["role"], "content": mensaje["content"]}
        for mensaje in st.session_state.mensajes[:-1]
    ]


def _mostrar_fuentes() -> None:
    st.header("Fuentes")
    if not st.session_state.fuentes:
        st.caption("Sin consulta activa.")
        return

    for resultado in st.session_state.fuentes:
        similitud = resultado.get("similitud")
        etiqueta_similitud = f" ({similitud:.3f})" if similitud is not None else ""
        with st.expander(
            f"{resultado['archivo']} - página {resultado['pagina']}{etiqueta_similitud}"
        ):
            if resultado.get("url"):
                st.link_button("Abrir fuente oficial", resultado["url"])
            st.write(resultado["texto"])


def _responder(consulta: str, resultados: list[dict], historial: list[dict]) -> str:
    if preguntar_stream is None:
        return preguntar(consulta, resultados, historial)

    acumulado = ""
    marcador = st.empty()
    try:
        for pedazo in preguntar_stream(consulta, resultados, historial):
            acumulado += pedazo
            marcador.markdown(f"{acumulado}▌")
    except Exception:
        if acumulado:
            raise
        respuesta = preguntar(consulta, resultados, historial)
        marcador.markdown(respuesta)
        return respuesta

    respuesta = acumulado.strip()
    marcador.markdown(respuesta)
    return respuesta


st.set_page_config(page_title="RAG Electiva II", layout="wide")
_inicializar_estado()

st.title("RAG Electiva II")

with st.sidebar:
    st.header("Documentos")
    uploads = st.file_uploader(
        "Cargar PDFs",
        type=["pdf"],
        accept_multiple_files=True,
    )

    if st.button("Indexar documentos", use_container_width=True):
        guardados = _guardar_uploads(uploads or [])
        paginas, chunks, nuevos = _indexar_documentos()
        detalle_uploads = ", ".join(guardados) if guardados else "sin archivos nuevos"
        st.session_state.ultima_indexacion = (
            f"{detalle_uploads}; {paginas} páginas, {chunks} chunks, "
            f"{nuevos} chunks nuevos"
        )

    if st.session_state.ultima_indexacion:
        st.success(st.session_state.ultima_indexacion)

    pdfs = _listar_pdfs()
    st.metric("PDFs en data/pdfs", len(pdfs))
    for pdf in pdfs:
        st.caption(pdf.name)

    st.metric("Chunks en BD", contar())
    ok_lm, detalle_lm = lmstudio_disponible()
    st.write(f"LMStudio: {'ON' if ok_lm else 'OFF'}")
    st.caption(detalle_lm)

    st.divider()
    if st.button("Limpiar conversación", use_container_width=True):
        st.session_state.mensajes = []
        st.session_state.fuentes = []
        st.rerun()

    if st.button("Limpiar base de datos", use_container_width=True):
        limpiar()
        st.session_state.fuentes = []
        st.session_state.ultima_indexacion = ""
        st.rerun()

    st.divider()
    _mostrar_fuentes()

for mensaje in st.session_state.mensajes:
    with st.chat_message(mensaje["role"]):
        st.markdown(mensaje["content"])

if pdfs and not st.session_state.mensajes:
    columnas = st.columns(len(PREGUNTAS_SUGERIDAS))
    for columna, pregunta in zip(columnas, PREGUNTAS_SUGERIDAS):
        if columna.button(pregunta, use_container_width=True):
            st.session_state.pregunta_sugerida = pregunta
            st.rerun()

consulta = st.session_state.pop("pregunta_sugerida", None)
entrada = st.chat_input("Preguntar sobre los PDFs indexados")
if entrada:
    consulta = entrada

if consulta:
    st.session_state.mensajes.append({"role": "user", "content": consulta})
    with st.chat_message("user"):
        st.markdown(consulta)

    resultados = buscar(consulta)
    st.session_state.fuentes = resultados
    historial = _historial_para_llm()

    with st.chat_message("assistant"):
        try:
            respuesta = _responder(consulta, resultados, historial)
        except Exception as exc:
            respuesta = f"Error al consultar LMStudio: {exc}"
            st.markdown(respuesta)

    st.session_state.mensajes.append({"role": "assistant", "content": respuesta})
