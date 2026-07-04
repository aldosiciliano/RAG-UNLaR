# RAG-UNLaR

A Retrieval-Augmented Generation (RAG) system built with ChromaDB, sentence-transformers, and LMStudio. It vectorizes PDF documents and generates contextualized responses through a local LLM, displaying the exact source fragments used for each answer.

---

## What it does

Instead of relying on what a language model has memorized during training, RAG-UNLaR retrieves relevant fragments from a local document database before generating a response. The user sees both the LLM's answer and the exact source — document name, page number, and official URL — that grounded it.

This means the system can answer accurately about documents the model has never seen, and every response is traceable back to a specific page of a specific file.

---

## Case study — Argentine AI Legislation

The current knowledge base contains five bills on Artificial Intelligence presented before the **Honorable Congreso de la Nación Argentina**, totaling 113 pages and 406 indexed chunks.

| Expediente | Title | Pages | Source |
|---|---|---|---|
| 290085 | Regulación General de IA — Dip. Giuliano | 15 | [hcdn.gob.ar](https://rest.hcdn.gob.ar/web/proyectos/290085/adjuntos/104681) |
| 3003-D-2024 | Régimen Jurídico para el Uso Responsable de la IA | 17 | [hcdn.gob.ar](https://www4.hcdn.gob.ar/dependencias/dsecretaria/Periodo2024/PDF2024/TP2024/3003-D-2024.pdf) |
| 1948-D-2025 | Reforma Ley 25.326 — Protección de Datos Personales y IA | 51 | [hcdn.gob.ar](https://www4.hcdn.gob.ar/dependencias/dsecretaria/Periodo2025/PDF2025/TP2025/1948-D-2025.pdf) |
| 0805-D-2024 | Responsabilidad Algorítmica y Promoción de la IA | 15 | [hcdn.gob.ar](https://www4.hcdn.gob.ar/dependencias/dsecretaria/Periodo2024/PDF2024/TP2024/0805-D-2024.pdf) |
| 1013-D-2024 | Ley Turing — Readecuación del Sistema Legal por Impacto de la IA | 15 | [hcdn.gob.ar](https://www4.hcdn.gob.ar/dependencias/dsecretaria/Periodo2024/PDF2024/TP2024/1013-D-2024.pdf) |

All documents are publicly available on the official Argentine Congress website and were not part of any LLM's training data, making them an ideal RAG use case.

---

## Built with

`Python 3.12` · `ChromaDB` · `sentence-transformers/all-MiniLM-L6-v2` · `LMStudio` · `google/gemma-3-1b` · `Streamlit` · `pdfplumber`

---

*Academic project — IA 2026 · Universidad Nacional de La Rioja (UNLaR)*
