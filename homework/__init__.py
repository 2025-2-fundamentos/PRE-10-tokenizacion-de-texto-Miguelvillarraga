"""Tokenización de texto - Taller PRE-10"""

import os
import re
from pathlib import Path
from dotenv import load_dotenv
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize

# Cargar variables de entorno
load_dotenv()

# Descargar recursos necesarios de NLTK
try:
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    nltk.download('punkt_tab')

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')


def get_config():
    """Obtener configuración desde .env"""
    return {
        'input_path': os.getenv('INPUT_PATH', 'files/input'),
        'output_path': os.getenv('OUTPUT_PATH', 'files/output'),
        'file_names': os.getenv('FILE_NAMES', 'file1.txt,file2.txt,file3.txt').split(','),
        'tokenizer_type': os.getenv('TOKENIZER_TYPE', 'word')
    }


def tokenize_text(text, tokenizer_type='word'):
    """
    Tokenizar texto según el tipo especificado.

    Args:
        text: Texto a tokenizar
        tokenizer_type: Tipo de tokenización ('word' o 'sentence')

    Returns:
        Lista de tokens
    """
    if tokenizer_type == 'sentence':
        return sent_tokenize(text)
    else:  # word
        # Limpiar el texto
        text = text.strip()
        # Tokenizar por palabras
        tokens = word_tokenize(text.lower())
        # Filtrar tokens vacíos y solo mantener palabras
        tokens = [token for token in tokens if token.isalnum()]
        return tokens


def process_files():
    """Procesar archivos de entrada y generar archivos tokenizados."""
    config = get_config()

    input_path = Path(config['input_path'])
    output_path = Path(config['output_path'])

    # Crear directorio de salida si no existe
    output_path.mkdir(parents=True, exist_ok=True)

    # Procesar cada archivo
    for file_name in config['file_names']:
        file_name = file_name.strip()
        input_file = input_path / file_name
        output_file = output_path / file_name

        if input_file.exists():
            # Leer archivo de entrada
            with open(input_file, 'r', encoding='utf-8') as f:
                text = f.read()

            # Tokenizar
            tokens = tokenize_text(text, config['tokenizer_type'])

            # Escribir archivo de salida
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write('\n'.join(tokens))

            print(f"✓ Procesado: {file_name} ({len(tokens)} tokens)")
        else:
            print(f"✗ Archivo no encontrado: {input_file}")


# Ejecutar al importar el módulo
process_files()
