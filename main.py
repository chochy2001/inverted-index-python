"""Demo del índice invertido — punto de entrada principal.

Modos:
  python3 main.py          -> Demo automática (frases + archivo por defecto)
  python3 main.py -i       -> Modo interactivo
"""

import os
import sys

from inverted_index import InvertedIndex


def print_separator(title=""):
    """Imprime un separador visual."""
    print(f"\n{'='*60}")
    if title:
        print(f"  {title}")
        print(f"{'='*60}")


def show_index(index):
    """Muestra el índice invertido completo."""
    terms = index.get_all_terms()
    if not terms:
        print("\n  El índice está vacío. Carga un archivo primero.")
        return
    print(f"\nÍndice invertido ({len(terms)} términos):")
    print("-" * 40)
    for term in terms:
        doc_ids = sorted(index.get_index()[term])
        print(f"  {term:20s} -> {doc_ids}")


def show_documents(index):
    """Muestra todos los documentos cargados."""
    count = index.document_count()
    if count == 0:
        print("\n  No hay documentos cargados.")
        return
    print(f"\nDocumentos cargados ({count}):")
    print("-" * 40)
    for doc_id in range(1, count + 1):
        text = index.get_document(doc_id)
        if text:
            print(f"  Doc {doc_id}: {text}")


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


def print_menu():
    """Muestra el menú principal."""
    print("\n┌──────────────────────────────────────┐")
    print("│      ÍNDICE INVERTIDO - MENÚ         │")
    print("├──────────────────────────────────────┤")
    print("│  1. Cargar archivo de documentos     │")
    print("│  2. Agregar documento manualmente    │")
    print("│  3. Buscar términos                  │")
    print("│  4. Ver documentos cargados          │")
    print("│  5. Ver índice invertido             │")
    print("│  6. Ver términos disponibles         │")
    print("│  7. Limpiar y empezar de nuevo       │")
    print("│  0. Salir                            │")
    print("└──────────────────────────────────────┘")


def interactive_mode():
    """Modo interactivo con menú de opciones."""
    print_separator("ÍNDICE INVERTIDO — Modo Interactivo")
    print("  Escribe el número de la opción deseada.")
    print("  Usa AND entre términos para búsquedas combinadas.")
    print("  Ejemplo: 'gato AND perro' o simplemente 'gato perro'")

    idx = InvertedIndex()

    while True:
        print_menu()
        try:
            option = input("\n  Opción: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n\n  ¡Hasta luego!")
            break

        if option == "0":
            print("\n  ¡Hasta luego!")
            break

        elif option == "1":
            default_file = os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                "data", "documentos.txt",
            )
            print("\n  Ingresa la ruta al archivo de texto (una frase por línea).")
            print(f"  Presiona Enter para usar el archivo por defecto:")
            print(f"    -> {default_file}")
            try:
                filepath = input("  Ruta: ").strip()
            except (EOFError, KeyboardInterrupt):
                print()
                continue

            if not filepath:
                filepath = default_file
                print(f"\n  Usando archivo por defecto: {filepath}")

            try:
                ids = idx.load_from_file(filepath)
                print(f"  Se cargaron {len(ids)} documentos desde '{filepath}'")
                print(f"  Total de documentos en el índice: {idx.document_count()}")

                show_documents(idx)

                terms = idx.get_all_terms()
                print(f"\n  Términos que puedes buscar ({len(terms)}):")
                print("  " + "-" * 38)
                cols = 4
                for i in range(0, len(terms), cols):
                    row = terms[i:i + cols]
                    print("  " + "".join(f"{t:20s}" for t in row))

                print("\n  Ejemplos de búsqueda:")
                print("    - Un término:    'datos'")
                print("    - AND implícito: 'inteligencia artificial'")
                print("    - AND explícito: 'datos AND análisis'")

            except FileNotFoundError:
                print(f"\n  Error: No se encontró el archivo '{filepath}'")
                print("  Verifica que la ruta sea correcta.")

        elif option == "2":
            print("\n  Escribe el texto del documento (vacío para cancelar):")
            try:
                text = input("  > ").strip()
            except (EOFError, KeyboardInterrupt):
                print()
                continue

            if not text:
                print("  Texto vacío, operación cancelada.")
                continue

            doc_id = idx.add_document(text)
            print(f"  Documento agregado con ID: {doc_id}")

        elif option == "3":
            if idx.document_count() == 0:
                print("\n  No hay documentos cargados. Usa la opción 1 o 2 primero.")
                continue

            print("\n  Escribe tu búsqueda (vacío para cancelar).")
            print("  Puedes usar AND: 'gato AND perro'")
            print("  O separar con espacios (AND implícito): 'gato perro'")

            while True:
                try:
                    query = input("\n  Buscar: ").strip()
                except (EOFError, KeyboardInterrupt):
                    print()
                    break

                if not query:
                    break

                show_search(idx, query)
                print("\n  (Escribe otra búsqueda o presiona Enter para volver)")

        elif option == "4":
            show_documents(idx)

        elif option == "5":
            show_index(idx)

        elif option == "6":
            terms = idx.get_all_terms()
            if not terms:
                print("\n  No hay términos. Carga documentos primero.")
            else:
                print(f"\n  Términos disponibles ({len(terms)}):")
                print("-" * 40)
                # Mostrar en columnas
                cols = 4
                for i in range(0, len(terms), cols):
                    row = terms[i:i + cols]
                    print("  " + "".join(f"{t:20s}" for t in row))

        elif option == "7":
            idx = InvertedIndex()
            print("\n  Índice reiniciado. Todos los documentos fueron eliminados.")

        else:
            print(f"\n  Opción '{option}' no válida. Elige entre 0 y 7.")


# --- Demo automática (modo original) ---

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
    if "-i" in sys.argv or "--interactive" in sys.argv:
        interactive_mode()
    else:
        demo_hardcoded()
        print("\n")
        demo_from_file()
