"""Módulo de índice invertido sin librerías de NLP."""

import re
import string
from collections import defaultdict


class InvertedIndex:
    """Índice invertido para búsqueda de documentos con soporte AND."""

    def __init__(self):
        self._index = defaultdict(set)
        self._documents = {}
        self._next_id = 1

    def _preprocess(self, text):
        """Normaliza texto: minúsculas, sin puntuación, split en tokens."""
        text = text.lower()
        text = text.translate(str.maketrans("", "", string.punctuation))
        tokens = text.split()
        return [t for t in tokens if t]

    def add_document(self, text):
        """Agrega un documento al índice y retorna su ID."""
        doc_id = self._next_id
        self._next_id += 1
        self._documents[doc_id] = text
        terms = self._preprocess(text)
        for term in terms:
            self._index[term].add(doc_id)
        return doc_id

    def add_documents(self, texts):
        """Agrega múltiples documentos al índice."""
        ids = []
        for text in texts:
            ids.append(self.add_document(text))
        return ids

    def load_from_file(self, filepath):
        """Carga documentos desde un archivo de texto (una frase por línea)."""
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                lines = f.readlines()
        except FileNotFoundError:
            raise FileNotFoundError(f"No se encontró el archivo: {filepath}")

        ids = []
        for line in lines:
            line = line.strip()
            if line:
                ids.append(self.add_document(line))
        return ids

    def search(self, query):
        """Busca documentos que contengan TODOS los términos de la query.

        Soporta:
        - "gato AND perro" (AND explícito)
        - "gato perro" (AND implícito entre todos los términos)
        """
        if not query or not query.strip():
            return []

        parts = re.split(r"\s+AND\s+", query, flags=re.IGNORECASE)

        all_terms = []
        for part in parts:
            terms = self._preprocess(part)
            all_terms.extend(terms)

        if not all_terms:
            return []

        result_sets = []
        for term in all_terms:
            if term not in self._index:
                return []
            result_sets.append(self._index[term])

        doc_ids = set.intersection(*result_sets)

        results = []
        for doc_id in sorted(doc_ids):
            results.append({"id": doc_id, "text": self._documents[doc_id]})
        return results

    def get_index(self):
        """Retorna el índice invertido como dict normal {término: set(ids)}."""
        return dict(self._index)

    def get_all_terms(self):
        """Retorna lista ordenada de todos los términos indexados."""
        return sorted(self._index.keys())

    def get_document(self, doc_id):
        """Retorna el texto de un documento por su ID."""
        return self._documents.get(doc_id)

    def document_count(self):
        """Retorna la cantidad total de documentos indexados."""
        return len(self._documents)
