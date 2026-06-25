import requests

from config import LMSTUDIO_BASE_URL, LMSTUDIO_MODEL, SYSTEM_PROMPT


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


def preguntar(consulta: str, chunks: list[dict], historial: list[dict] | None = None) -> str:
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

    respuesta = requests.post(
        f"{LMSTUDIO_BASE_URL}/chat/completions",
        json={
            "model": LMSTUDIO_MODEL,
            "messages": mensajes,
            "temperature": 0.1,
            "max_tokens": 500,
        },
        timeout=60,
    )
    respuesta.raise_for_status()
    data = respuesta.json()
    return data["choices"][0]["message"]["content"].strip()
