# Indice Invertido / Inverted Index

> **Idioma / Language:** [Español](#motor-de-búsqueda-con-índice-invertido) | [English](#inverted-index-search-engine)

---

## Motor de Búsqueda con Índice Invertido

Implementación en Python de un índice invertido con soporte de búsqueda usando el operador AND. Construido sin librerías de NLP — solo la biblioteca estándar de Python.

### Características

- **Preprocesamiento de texto**: conversión a minúsculas, eliminación de puntuación, tokenización
- **Búsqueda AND**: explícita (`gato AND perro`) e implícita (`gato perro`)
- **Insensible a mayúsculas/minúsculas** en queries y operadores
- **Modo interactivo**: menú con opciones para cargar archivos, buscar y explorar el índice
- **Archivo por defecto**: si no se especifica archivo, carga `data/documentos.txt` y muestra los términos disponibles
- **Carga desde archivo**: documentos desde cualquier archivo de texto (uno por línea)
- **Sin dependencias externas**: solo usa `re`, `string`, `collections`

### Estructura del Proyecto

```
├── inverted_index.py          # Clase InvertedIndex (lógica principal)
├── main.py                    # Demo, modo interactivo y punto de entrada
├── test_inverted_index.py     # Tests unitarios (unittest)
└── data/
    └── documentos.txt         # Documentos de ejemplo
```

### Uso

#### Modo interactivo

```bash
python3 main.py -i
```

Muestra un menú con las siguientes opciones:

```
┌──────────────────────────────────────┐
│      ÍNDICE INVERTIDO - MENÚ         │
├──────────────────────────────────────┤
│  1. Cargar archivo de documentos     │
│  2. Agregar documento manualmente    │
│  3. Buscar términos                  │
│  4. Ver documentos cargados          │
│  5. Ver índice invertido             │
│  6. Ver términos disponibles         │
│  7. Limpiar y empezar de nuevo       │
│  0. Salir                            │
└──────────────────────────────────────┘
```

Al cargar un archivo (opción 1), se puede presionar **Enter** sin escribir ruta para usar el archivo por defecto `data/documentos.txt`. Después de cargar, se muestran los documentos y todos los términos disponibles para buscar.

#### Demo automática

```bash
python3 main.py
```

Ejecuta una demostración con frases en memoria y con el archivo de ejemplo.

#### Usar como módulo

```python
from inverted_index import InvertedIndex

idx = InvertedIndex()
idx.add_documents([
    "El gato negro duerme en el sofá",
    "El perro juega con la pelota roja",
    "El gato y el perro son amigos",
])

# Búsqueda de un término
results = idx.search("gato")

# AND explícito
results = idx.search("gato AND perro")

# AND implícito (todos los términos deben estar presentes)
results = idx.search("pelota roja")

# Cargar desde archivo
idx.load_from_file("data/documentos.txt")
```

Cada resultado es un diccionario con `id` y `text`:

```python
[{"id": 1, "text": "El gato negro duerme en el sofá"}, ...]
```

#### Ejecutar tests

```bash
python3 -m unittest test_inverted_index.py -v
```

### Cómo Funciona

1. **Indexación**: cada documento se preprocesa (minúsculas, eliminar puntuación, tokenizar) y cada término se mapea al conjunto de IDs de documentos que lo contienen
2. **Búsqueda**: la query se divide por `AND` (insensible a mayúsculas), cada parte se preprocesa en términos, y la intersección de todos los conjuntos da los documentos coincidentes
3. **Resultados** se retornan ordenados por ID de documento

---

## Inverted Index Search Engine

A Python implementation of an inverted index that supports document search with the AND operator. Built without any NLP libraries — only Python's standard library.

### Features

- **Text preprocessing**: lowercasing, punctuation removal, tokenization
- **AND search**: explicit (`cat AND dog`) and implicit (`cat dog`)
- **Case insensitive** queries and operators
- **Interactive mode**: menu with options to load files, search and explore the index
- **Default file**: if no file is specified, loads `data/documentos.txt` and shows available terms
- **File loading**: load documents from any text file (one per line)
- **No external dependencies**: uses only `re`, `string`, `collections`

### Project Structure

```
├── inverted_index.py          # InvertedIndex class (core logic)
├── main.py                    # Demo, interactive mode and entry point
├── test_inverted_index.py     # Unit tests (unittest)
└── data/
    └── documentos.txt         # Sample documents
```

### Usage

#### Interactive mode

```bash
python3 main.py -i
```

Shows a menu with the following options:

```
┌──────────────────────────────────────┐
│      ÍNDICE INVERTIDO - MENÚ         │
├──────────────────────────────────────┤
│  1. Cargar archivo de documentos     │
│  2. Agregar documento manualmente    │
│  3. Buscar términos                  │
│  4. Ver documentos cargados          │
│  5. Ver índice invertido             │
│  6. Ver términos disponibles         │
│  7. Limpiar y empezar de nuevo       │
│  0. Salir                            │
└──────────────────────────────────────┘
```

When loading a file (option 1), you can press **Enter** without typing a path to use the default file `data/documentos.txt`. After loading, all documents and available search terms are displayed.

#### Automatic demo

```bash
python3 main.py
```

Runs a demonstration with in-memory phrases and the sample file.

#### Use as a module

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

#### Run tests

```bash
python3 -m unittest test_inverted_index.py -v
```

### How It Works

1. **Indexing**: each document is preprocessed (lowercase, remove punctuation, tokenize) and each term maps to the set of document IDs that contain it
2. **Searching**: the query is split by `AND` (case insensitive), each part is preprocessed into terms, and the intersection of all term sets gives the matching documents
3. **Results** are returned sorted by document ID
