"""Demo del índice invertido — punto de entrada principal."""

import os

from inverted_index import InvertedIndex


def print_separator(title=""):
    """Imprime un separador visual."""
    print(f"\n{'='*60}")
    if title:
        print(f"  {title}")
        print(f"{'='*60}")


def show_index(index):
    """Muestra el índice invertido completo."""
    print("\nÍndice invertido:")
    print("-" * 40)
    for term in index.get_all_terms():
        doc_ids = sorted(index.get_index()[term])
        print(f"  {term:20s} -> {doc_ids}")


def show_search(index, query):
    """Ejecuta y muestra los resultados de una búsqueda."""
    print(f'\nBúsqueda: "{query}"')
    results = index.search(query)
    if results:
        print(f"  Resultados ({len(results)}):")
        for r in results:
            print(f"    Doc {r['id']}: {r['text']}")
    else:
        print("  Sin resultados.")


def demo_hardcoded():
    """Demo con frases hardcodeadas."""
    print_separator("DEMO 1: Frases en memoria")

    frases = [
        "El gato negro duerme en el sofá",
        "El perro juega con la pelota roja",
        "El gato y el perro son amigos",
        "La pelota roja está debajo del sofá",
        "El pájaro canta en el árbol verde",
        "El gato negro caza ratones en el jardín",
    ]

    idx = InvertedIndex()
    for i, frase in enumerate(frases, 1):
        idx.add_document(frase)
        print(f"  Doc {i}: {frase}")

    show_index(idx)

    queries = [
        "gato",
        "gato AND negro",
        "pelota roja",
        "gato AND perro",
        "sofá",
        "dinosaurio",
        "el",
    ]

    print_separator("Búsquedas")
    for q in queries:
        show_search(idx, q)


def demo_from_file():
    """Demo cargando documentos desde archivo."""
    print_separator("DEMO 2: Carga desde archivo")

    filepath = os.path.join(os.path.dirname(__file__), "data", "documentos.txt")

    idx = InvertedIndex()
    try:
        ids = idx.load_from_file(filepath)
        print(f"  Se cargaron {len(ids)} documentos desde {filepath}")

        print("\nDocumentos cargados:")
        for doc_id in ids:
            print(f"  Doc {doc_id}: {idx.get_document(doc_id)}")

        show_index(idx)

        queries = [
            "inteligencia artificial",
            "datos AND análisis",
            "programación",
            "python AND datos",
            "redes AND seguridad",
        ]

        print_separator("Búsquedas sobre archivo")
        for q in queries:
            show_search(idx, q)

    except FileNotFoundError as e:
        print(f"  Error: {e}")


if __name__ == "__main__":
    demo_hardcoded()
    print("\n")
    demo_from_file()
