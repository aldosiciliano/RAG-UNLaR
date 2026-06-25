import streamlit as st

from config import PDF_DIR
from modules.llm import lmstudio_disponible, preguntar
from modules.retrieval import buscar
from modules.vectorstore import contar

st.set_page_config(page_title="RAG Electiva II", layout="wide")

st.title("RAG Electiva II")

with st.sidebar:
    st.header("Estado")
    pdfs = sorted(PDF_DIR.glob("*.pdf")) if PDF_DIR.exists() else []
    st.metric("PDFs indexados", len(pdfs))
    for pdf in pdfs:
        st.caption(pdf.name)

    st.metric("Chunks en BD", contar())
    ok_lm, detalle_lm = lmstudio_disponible()
    st.write(f"LMStudio: {'✓ ON' if ok_lm else '✗ OFF'}")
    st.caption(detalle_lm)

if "mensajes" not in st.session_state:
    st.session_state.mensajes = []

for mensaje in st.session_state.mensajes:
    with st.chat_message(mensaje["role"]):
        st.markdown(mensaje["content"])

consulta = st.chat_input("Preguntar sobre los PDFs indexados")
if consulta:
    st.session_state.mensajes.append({"role": "user", "content": consulta})
    with st.chat_message("user"):
        st.markdown(consulta)

    resultados = buscar(consulta)
    historial = [
        {"role": m["role"], "content": m["content"]}
        for m in st.session_state.mensajes[:-1]
    ]

    try:
        respuesta = preguntar(consulta, resultados, historial)
    except Exception as exc:
        respuesta = f"Error al consultar LMStudio: {exc}"

    st.session_state.mensajes.append({"role": "assistant", "content": respuesta})
    with st.chat_message("assistant"):
        st.markdown(respuesta)

    with st.sidebar:
        st.header("Fuentes")
        for resultado in resultados:
            with st.expander(
                f"{resultado['archivo']} - página {resultado['pagina']} "
                f"({resultado['similitud']:.3f})"
            ):
                st.write(resultado["texto"])
