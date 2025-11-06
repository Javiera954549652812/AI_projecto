import re
import sys
import difflib
from collections import Counter
from math import sqrt

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Sistema básico de recomendación de películas de Harry Potter
# Archivo: recomendacion_sistema.py
# GitHub Copilot


# Pequeña base de datos propia (descripciones cortas originales, no copiadas)
MOVIES = [
    {
        "title": "Harry Potter y la piedra filosofal",
        "year": 2001,
        "genres": ["Aventura", "Fantasía", "Familiar"],
        "director": "Chris Columbus",
        "cast": ["Daniel Radcliffe", "Emma Watson", "Rupert Grint"],
        "summary": "Un niño descubre que es mago y empieza sus estudios en una escuela de magia."
    },
    {
        "title": "Harry Potter y la cámara secreta",
        "year": 2002,
        "genres": ["Aventura", "Fantasía", "Misterio"],
        "director": "Chris Columbus",
        "cast": ["Daniel Radcliffe", "Emma Watson", "Rupert Grint"],
        "summary": "Un misterio en la escuela pone en peligro a los estudiantes y a la comunidad mágica."
    },
    {
        "title": "Harry Potter y el prisionero de Azkaban",
        "year": 2004,
        "genres": ["Aventura", "Fantasía", "Terror leve"],
        "director": "Alfonso Cuarón",
        "cast": ["Daniel Radcliffe", "Emma Watson", "Rupert Grint"],
        "summary": "Aparecen secretos del pasado y un prisionero fugitivo cambia el rumbo de la historia."
    },
    {
        "title": "Harry Potter y el cáliz de fuego",
        "year": 2005,
        "genres": ["Aventura", "Fantasía", "Acción"],
        "director": "Mike Newell",
        "cast": ["Daniel Radcliffe", "Emma Watson", "Rupert Grint"],
        "summary": "Un torneo peligroso enfrenta a jóvenes magos de distintas escuelas."
    },
    {
        "title": "Harry Potter y la Orden del Fénix",
        "year": 2007,
        "genres": ["Aventura", "Fantasía", "Drama"],
        "director": "David Yates",
        "cast": ["Daniel Radcliffe", "Emma Watson", "Rupert Grint"],
        "summary": "La comunidad mágica enfrenta amenazas internas mientras el protagonista madura."
    },
    {
        "title": "Harry Potter y el misterio del príncipe",
        "year": 2009,
        "genres": ["Aventura", "Fantasía", "Romance"],
        "director": "David Yates",
        "cast": ["Daniel Radcliffe", "Emma Watson", "Rupert Grint"],
        "summary": "Se revelan pistas cruciales sobre el enemigo y las lealtades se ponen a prueba."
    },
    {
        "title": "Harry Potter y las Reliquias de la Muerte - Parte 1",
        "year": 2010,
        "genres": ["Aventura", "Fantasía", "Acción"],
        "director": "David Yates",
        "cast": ["Daniel Radcliffe", "Emma Watson", "Rupert Grint"],
        "summary": "La búsqueda de objetos clave obliga a los protagonistas a abandonar la escuela."
    },
    {
        "title": "Harry Potter y las Reliquias de la Muerte - Parte 2",
        "year": 2011,
        "genres": ["Aventura", "Fantasía", "Épico"],
        "director": "David Yates",
        "cast": ["Daniel Radcliffe", "Emma Watson", "Rupert Grint"],
        "summary": "El enfrentamiento final decide el destino del mundo mágico."
    },
]

# Tokenización simple (quita puntuación y divide por espacios)
_WORD_RE = re.compile(r"\w+", flags=re.UNICODE)

def tokenize(text):
    text = text.lower()
    return _WORD_RE.findall(text)

def movie_profile(movie):
    """
    Crea un perfil de tokens ponderados para una película.
    - summary: tokens con peso 1
    - genres: tokens con peso 2
    - director: tokens con peso 2
    - cast: tokens con peso 2 cada miembro
    Devuelve Counter (vector de frecuencias).
    """
    tokens = []
    tokens += tokenize(movie.get("summary", ""))  # peso 1
    for g in movie.get("genres", []):
        tokens += tokenize(g) * 2
    tokens += tokenize(movie.get("director", "")) * 2
    for member in movie.get("cast", []):
        tokens += tokenize(member) * 2
    return Counter(tokens)

def cosine_similarity(counter_a, counter_b):
    """Cosine similarity entre dos Counters (vectores esparcidos)."""
    if not counter_a or not counter_b:
        return 0.0
    # intersección de claves
    intersection = set(counter_a.keys()) & set(counter_b.keys())
    num = sum(counter_a[k] * counter_b[k] for k in intersection)
    sum1 = sum(v * v for v in counter_a.values())
    sum2 = sum(v * v for v in counter_b.values())
    denom = sqrt(sum1) * sqrt(sum2)
    if denom == 0:
        return 0.0
    return num / denom

# Precomputar perfiles
PROFILES = {m["title"]: movie_profile(m) for m in MOVIES}

def recommend(title, k=3):
    """Devuelve las k películas más similares a 'title' (excluye la película misma)."""
    if title not in PROFILES:
        # sugerir títulos similares
        matches = difflib.get_close_matches(title, PROFILES.keys(), n=5, cutoff=0.4)
        raise ValueError(f"Título no encontrado. Sugerencias: {matches}")
    base = PROFILES[title]
    sims = []
    for t, profile in PROFILES.items():
        if t == title:
            continue
        sims.append((t, cosine_similarity(base, profile)))
    sims.sort(key=lambda x: x[1], reverse=True)
    return sims[:k]

def print_recommendations(title, k=3):
    try:
        recs = recommend(title, k)
    except ValueError as e:
        print(e)
        return
    print(f"Recomendaciones para '{title}':")
    for idx, (t, score) in enumerate(recs, 1):
        print(f"{idx}. {t} (similitud: {score:.3f})")

def list_titles():
    for m in MOVIES:
        print(f"- {m['title']} ({m['year']})")

def main(argv):
    if len(argv) == 1:
        print("Sistema básico de recomendación de películas de Harry Potter")
        print("Disponibles:")
        list_titles()
        print("\nUso:\n  python recomendacion_sistema.py \"Título de la película\" [k]")
        return
    title = argv[1]
    k = int(argv[2]) if len(argv) > 2 else 3
    print_recommendations(title, k)

if __name__ == "__main__":
    main(sys.argv)