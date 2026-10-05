import os
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent.parent

# Diretórios de Dados
DATA_DIR = ROOT_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
RESULTS_DIR = DATA_DIR / "results"

RAW_PT_DIR = RAW_DIR / "pt-br"
RAW_EN_DIR = RAW_DIR / "eng"

PROCESSED_PT_FILE = PROCESSED_DIR / "corpus_pt.txt"
PROCESSED_EN_FILE = PROCESSED_DIR / "corpus_en.txt"

RESULTS_PT_FILE = RESULTS_DIR / "counts_pt.csv"
RESULTS_EN_FILE = RESULTS_DIR / "counts_en.csv"

# Binários e Código C
BIN_DIR = ROOT_DIR / "bin"
SCANNER_BIN = BIN_DIR / ("scanner.exe" if os.name == "nt" else "scanner")
SCANNER_SRC = ROOT_DIR / "src" / "c" / "scanner.c"

# Diretório de Saída (Gráficos e Imagens)
OUT_DIR = ROOT_DIR / "out"
FIGURES_DIR = OUT_DIR
