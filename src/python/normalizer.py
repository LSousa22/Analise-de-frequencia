import os
import re
import unicodedata
from pathlib import Path

def remove_diacritics(text: str) -> str:
    """
    Remove acentos e diacríticos de uma string utilizando decomposição NFKD.
    Exemplo: 'ã' -> 'a', 'é' -> 'e', 'ç' -> 'c'.
    """
    nfkd = unicodedata.normalize('NFKD', text)
    return "".join(c for c in nfkd if not unicodedata.combining(c))

def normalize_pattern(pattern: str) -> str:
    """
    Normaliza uma sequência-alvo (digrama/trigrama):
    - Converte para minúsculas;
    - Remove diacríticos;
    - Remove espaços e caracteres não alfabéticos.
    """
    cleaned = remove_diacritics(pattern.strip().lower())
    matches = re.findall(r'[a-z]+', cleaned)
    return "".join(matches)

def normalize_text(text: str) -> list[str]:
    """
    Normaliza um texto completo:
    - Converte para minúsculas;
    - Remove diacríticos e acentos via NFKD;
    - Isola as palavras removendo pontuações, números e caracteres especiais,
      mantendo apenas caracteres alfabéticos válidos [a-z]+.
    """
    cleaned = remove_diacritics(text.lower())
    return re.findall(r'[a-z]+', cleaned)

def normalize_single_file(input_file: Path, output_file: Path) -> int:
    """
    Normaliza um único arquivo de texto e grava o resultado formatado.
    Retorna o número de palavras normalizadas.
    """
    in_path = Path(input_file)
    out_path = Path(output_file)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    with open(in_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    words = normalize_text(content)
    with open(out_path, "w", encoding="utf-8") as out:
        out.write(f"# DOC: {in_path.name}\n")
        if words:
            out.write(" ".join(words) + "\n")

    return len(words)

def build_consolidated_corpus(input_dir: Path, output_file: Path) -> int:
    """
    Lê todos os arquivos .txt do diretório de entrada, normaliza suas palavras
    e gera um único arquivo consolidado com delimitadores de documento (# DOC: ...).
    Retorna o total de palavras analisadas no corpus.
    """
    input_path = Path(input_dir)
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    total_words = 0
    txt_files = sorted(list(input_path.glob("*.txt")))

    with open(output_path, "w", encoding="utf-8") as out:
        for file in txt_files:
            out.write(f"# DOC: {file.name}\n")
            with open(file, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            words = normalize_text(content)
            total_words += len(words)
            if words:
                out.write(" ".join(words) + "\n")

    return total_words

if __name__ == "__main__":
    try:
        from src.python.config import RAW_PT_DIR, RAW_EN_DIR, PROCESSED_PT_FILE, PROCESSED_EN_FILE
    except ImportError:
        RAW_PT_DIR = Path("data/raw/pt-br")
        RAW_EN_DIR = Path("data/raw/eng")
        PROCESSED_PT_FILE = Path("data/processed/corpus_pt.txt")
        PROCESSED_EN_FILE = Path("data/processed/corpus_en.txt")

    if RAW_PT_DIR.exists() and any(RAW_PT_DIR.glob("*.txt")):
        count = build_consolidated_corpus(RAW_PT_DIR, PROCESSED_PT_FILE)
        print(f"Corpus PT consolidado: {count} palavras.")

    if RAW_EN_DIR.exists() and any(RAW_EN_DIR.glob("*.txt")):
        count = build_consolidated_corpus(RAW_EN_DIR, PROCESSED_EN_FILE)
        print(f"Corpus EN consolidado: {count} palavras.")
