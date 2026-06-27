import json

import requests
from config import LMSTUDIO_BASE_URL, LMSTUDIO_MODEL, SYSTEM_PROMPT

TEMPERATURE = 0.1
MAX_TOKENS = 500
REQUEST_TIMEOUT = 60


def lmstudio_disponible() -> tuple[bool, str]:
    try:
        respuesta = requests.get(f"{LMSTUDIO_BASE_URL}/models", timeout=5)
        respuesta.raise_for_status()
        modelos = respuesta.json().get("data", [])
        if not modelos:
            return False, "Sin modelos cargados"
        return True, modelos[0].get("id", "modelo local")
    except requests.RequestException as exc:
        return False, str(exc)


def construir_mensajes(
    consulta: str,
    chunks: list[dict],
    historial: list[dict] | None = None,
) -> list[dict]:
    historial = historial or []
    contexto = "\n\n".join(
        f"Fuente: {chunk['archivo']} página {chunk['pagina']}\n{chunk['texto']}"
        for chunk in chunks
    )

    mensajes = [{"role": "system", "content": SYSTEM_PROMPT}]
    mensajes.extend(historial[-6:])
    mensajes.append(
        {
            "role": "user",
            "content": (
                "Contexto recuperado:\n"
                f"{contexto}\n\n"
                f"Pregunta: {consulta}\n"
                "Respondé en español y citá página cuando sea útil."
            ),
        }
    )
    return mensajes


def preguntar(
    consulta: str, chunks: list[dict], historial: list[dict] | None = None
) -> str:
    mensajes = construir_mensajes(consulta, chunks, historial)

    respuesta = requests.post(
        f"{LMSTUDIO_BASE_URL}/chat/completions",
        json={
            "model": LMSTUDIO_MODEL,
            "messages": mensajes,
            "temperature": TEMPERATURE,
            "max_tokens": MAX_TOKENS,
        },
        timeout=REQUEST_TIMEOUT,
    )
    respuesta.raise_for_status()
    data = respuesta.json()
    return data["choices"][0]["message"]["content"].strip()


def preguntar_stream(
    consulta: str,
    chunks: list[dict],
    historial: list[dict] | None = None,
):
    mensajes = construir_mensajes(consulta, chunks, historial)

    with requests.post(
        f"{LMSTUDIO_BASE_URL}/chat/completions",
        json={
            "model": LMSTUDIO_MODEL,
            "messages": mensajes,
            "temperature": TEMPERATURE,
            "max_tokens": MAX_TOKENS,
            "stream": True,
        },
        timeout=REQUEST_TIMEOUT,
        stream=True,
    ) as respuesta:
        respuesta.raise_for_status()
        for linea in respuesta.iter_lines(decode_unicode=True):
            if not linea:
                continue
            if linea.startswith("data: "):
                linea = linea.removeprefix("data: ").strip()
            if linea == "[DONE]":
                break

            try:
                data = json.loads(linea)
            except ValueError:
                continue

            delta = data.get("choices", [{}])[0].get("delta", {})
            contenido = delta.get("content")
            if contenido:
                yield contenido
