"""Tests unitarios para InvertedIndex."""

import os
import tempfile
import unittest

from inverted_index import InvertedIndex


class TestInvertedIndex(unittest.TestCase):
    """Suite de pruebas para la clase InvertedIndex."""

    def setUp(self):
        """Prepara un índice con documentos de prueba."""
        self.idx = InvertedIndex()
        self.idx.add_documents([
            "El gato negro duerme en el sofá",        # Doc 1
            "El perro juega con la pelota roja",       # Doc 2
            "El gato y el perro son amigos",           # Doc 3
            "La pelota roja está debajo del sofá",     # Doc 4
            "El pájaro canta en el árbol verde",       # Doc 5
        ])

    def test_add_document_returns_id(self):
        """add_document retorna un ID incremental."""
        idx = InvertedIndex()
        self.assertEqual(idx.add_document("primer documento"), 1)
        self.assertEqual(idx.add_document("segundo documento"), 2)

    def test_add_documents_returns_ids(self):
        """add_documents retorna lista de IDs."""
        idx = InvertedIndex()
        ids = idx.add_documents(["uno", "dos", "tres"])
        self.assertEqual(ids, [1, 2, 3])

    def test_document_count(self):
        """document_count retorna la cantidad correcta."""
        self.assertEqual(self.idx.document_count(), 5)

    def test_get_document(self):
        """get_document retorna el texto original."""
        self.assertEqual(
            self.idx.get_document(1), "El gato negro duerme en el sofá"
        )

    def test_get_document_not_found(self):
        """get_document retorna None para ID inexistente."""
        self.assertIsNone(self.idx.get_document(999))

    def test_search_single_term(self):
        """Búsqueda de un solo término retorna documentos correctos."""
        results = self.idx.search("gato")
        ids = [r["id"] for r in results]
        self.assertEqual(ids, [1, 3])

    def test_search_and_explicit(self):
        """Búsqueda con AND explícito funciona correctamente."""
        results = self.idx.search("gato AND perro")
        ids = [r["id"] for r in results]
        self.assertEqual(ids, [3])

    def test_search_and_implicit(self):
        """Búsqueda con múltiples palabras usa AND implícito."""
        results = self.idx.search("pelota roja")
        ids = [r["id"] for r in results]
        self.assertEqual(ids, [2, 4])

    def test_search_no_results(self):
        """Búsqueda de término inexistente retorna lista vacía."""
        results = self.idx.search("dinosaurio")
        self.assertEqual(results, [])

    def test_search_case_insensitive(self):
        """La búsqueda no distingue mayúsculas/minúsculas."""
        results_lower = self.idx.search("gato")
        results_upper = self.idx.search("GATO")
        results_mixed = self.idx.search("Gato")
        self.assertEqual(results_lower, results_upper)
        self.assertEqual(results_lower, results_mixed)

    def test_search_and_case_insensitive(self):
        """El operador AND funciona sin importar mayúsculas."""
        r1 = self.idx.search("gato AND perro")
        r2 = self.idx.search("gato and perro")
        r3 = self.idx.search("gato And perro")
        self.assertEqual(r1, r2)
        self.assertEqual(r1, r3)

    def test_search_with_punctuation(self):
        """La búsqueda ignora puntuación en la query."""
        idx = InvertedIndex()
        idx.add_document("Hola, mundo!")
        results = idx.search("hola, mundo!")
        self.assertEqual(len(results), 1)

    def test_search_empty_query(self):
        """Query vacía retorna lista vacía."""
        self.assertEqual(self.idx.search(""), [])
        self.assertEqual(self.idx.search("   "), [])

    def test_search_partial_no_match(self):
        """AND con un término sin match retorna vacío."""
        results = self.idx.search("gato AND dinosaurio")
        self.assertEqual(results, [])

    def test_get_all_terms_sorted(self):
        """get_all_terms retorna términos en orden alfabético."""
        terms = self.idx.get_all_terms()
        self.assertEqual(terms, sorted(terms))
        self.assertIn("gato", terms)
        self.assertIn("perro", terms)

    def test_get_index_structure(self):
        """get_index retorna dict con sets de IDs."""
        index = self.idx.get_index()
        self.assertIsInstance(index, dict)
        self.assertIsInstance(index["gato"], set)
        self.assertEqual(index["gato"], {1, 3})

    def test_load_from_file(self):
        """load_from_file carga documentos correctamente."""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".txt", delete=False, encoding="utf-8"
        ) as f:
            f.write("primera línea\n")
            f.write("segunda línea\n")
            f.write("\n")
            f.write("tercera línea\n")
            tmppath = f.name

        try:
            idx = InvertedIndex()
            ids = idx.load_from_file(tmppath)
            self.assertEqual(len(ids), 3)
            self.assertEqual(idx.document_count(), 3)
        finally:
            os.unlink(tmppath)

    def test_load_from_file_not_found(self):
        """load_from_file lanza FileNotFoundError si no existe."""
        idx = InvertedIndex()
        with self.assertRaises(FileNotFoundError):
            idx.load_from_file("/ruta/que/no/existe.txt")

    def test_results_ordered_by_id(self):
        """Los resultados se retornan ordenados por ID de documento."""
        results = self.idx.search("el")
        ids = [r["id"] for r in results]
        self.assertEqual(ids, sorted(ids))

    def test_results_contain_text(self):
        """Cada resultado contiene id y text."""
        results = self.idx.search("gato")
        for r in results:
            self.assertIn("id", r)
            self.assertIn("text", r)
            self.assertIsInstance(r["id"], int)
            self.assertIsInstance(r["text"], str)


if __name__ == "__main__":
    unittest.main()
