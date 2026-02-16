# Inverted Index Search Engine

A Python implementation of an inverted index that supports document search with the AND operator. Built without any NLP libraries — only Python's standard library.

## Features

- **Text preprocessing**: lowercasing, punctuation removal, tokenization
- **AND search**: explicit (`cat AND dog`) and implicit (`cat dog`)
- **Case insensitive** queries and operators
- **File loading**: load documents from a text file (one per line)
- **No external dependencies**: uses only `re`, `string`, `collections`

## Project Structure

```
├── inverted_index.py          # InvertedIndex class (core logic)
├── main.py                    # Demo and entry point
├── test_inverted_index.py     # Unit tests (unittest)
└── data/
    └── documentos.txt         # Sample documents
```

## Usage

### Run the demo

```bash
python3 main.py
```

### Use as a module

```python
from inverted_index import InvertedIndex

idx = InvertedIndex()
idx.add_documents([
    "The black cat sleeps on the sofa",
    "The dog plays with the red ball",
    "The cat and the dog are friends",
])

# Single term search
results = idx.search("cat")

# Explicit AND
results = idx.search("cat AND dog")

# Implicit AND (all terms must be present)
results = idx.search("red ball")

# Load from file
idx.load_from_file("data/documentos.txt")
```

Each result is a dictionary with `id` and `text`:

```python
[{"id": 1, "text": "The black cat sleeps on the sofa"}, ...]
```

### Run tests

```bash
python3 -m unittest test_inverted_index.py -v
```

## How It Works

1. **Indexing**: each document is preprocessed (lowercase, remove punctuation, tokenize) and each term maps to the set of document IDs that contain it
2. **Searching**: the query is split by `AND` (case insensitive), each part is preprocessed into terms, and the intersection of all term sets gives the matching documents
3. **Results** are returned sorted by document ID

---

# Motor de Busqueda con Indice Invertido

Implementacion en Python de un indice invertido con soporte de busqueda usando el operador AND. Construido sin librerias de NLP — solo la biblioteca estandar de Python.

## Caracteristicas

- **Preprocesamiento de texto**: conversion a minusculas, eliminacion de puntuacion, tokenizacion
- **Busqueda AND**: explicita (`gato AND perro`) e implicita (`gato perro`)
- **Insensible a mayusculas/minusculas** en queries y operadores
- **Carga desde archivo**: documentos desde un archivo de texto (uno por linea)
- **Sin dependencias externas**: solo usa `re`, `string`, `collections`

## Estructura del Proyecto

```
├── inverted_index.py          # Clase InvertedIndex (logica principal)
├── main.py                    # Demo y punto de entrada
├── test_inverted_index.py     # Tests unitarios (unittest)
└── data/
    └── documentos.txt         # Documentos de ejemplo
```

## Uso

### Ejecutar la demo

```bash
python3 main.py
```

### Usar como modulo

```python
from inverted_index import InvertedIndex

idx = InvertedIndex()
idx.add_documents([
    "El gato negro duerme en el sofa",
    "El perro juega con la pelota roja",
    "El gato y el perro son amigos",
])

# Busqueda de un termino
results = idx.search("gato")

# AND explicito
results = idx.search("gato AND perro")

# AND implicito (todos los terminos deben estar presentes)
results = idx.search("pelota roja")

# Cargar desde archivo
idx.load_from_file("data/documentos.txt")
```

Cada resultado es un diccionario con `id` y `text`:

```python
[{"id": 1, "text": "El gato negro duerme en el sofa"}, ...]
```

### Ejecutar tests

```bash
python3 -m unittest test_inverted_index.py -v
```

## Como Funciona

1. **Indexacion**: cada documento se preprocesa (minusculas, eliminar puntuacion, tokenizar) y cada termino se mapea al conjunto de IDs de documentos que lo contienen
2. **Busqueda**: la query se divide por `AND` (insensible a mayusculas), cada parte se preprocesa en terminos, y la interseccion de todos los conjuntos da los documentos coincidentes
3. **Resultados** se retornan ordenados por ID de documento
