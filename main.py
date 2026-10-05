import sys
import subprocess
import argparse
from pathlib import Path

from src.python.config import (
    RAW_PT_DIR, RAW_EN_DIR,
    PROCESSED_PT_FILE, PROCESSED_EN_FILE,
    RESULTS_PT_FILE, RESULTS_EN_FILE,
    SCANNER_BIN, SCANNER_SRC,
    OUT_DIR
)
from src.python.normalizer import build_consolidated_corpus, normalize_single_file
from src.python.analytics import (
    load_counts, compute_metrics,
    print_report, plot_frequencies,
    generate_comparison_plot
)

def compile_c_scanner_if_needed():
    """Compila o motor em C caso o binário não exista."""
    if not SCANNER_BIN.exists():
        print("[Build] Executável do scanner não encontrado. Compilando com GCC...")
        SCANNER_BIN.parent.mkdir(parents=True, exist_ok=True)
        cmd = ["gcc", "-Wall", "-Wextra", "-O3", str(SCANNER_SRC), "-o", str(SCANNER_BIN)]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode != 0:
            print(f"[Build Error] Falha na compilação do C:\n{res.stderr}", file=sys.stderr)
            sys.exit(1)
        print("[Build] Compilação concluída com sucesso.")

def analyze_single_file(file_path: Path, lang: str):
    """Executa a análise isolada de um único texto."""
    target_file = Path(file_path)
    if not target_file.exists():
        print(f"[Erro] Arquivo não encontrado: {target_file}", file=sys.stderr)
        sys.exit(1)

    compile_c_scanner_if_needed()

    normalized_out = Path("data/processed") / f"single_{target_file.stem}.txt"
    counts_out = Path("data/results") / f"single_{target_file.stem}_counts.csv"
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    figure_out = OUT_DIR / f"single_{target_file.stem}.png"

    print(f"\n--- [Análise Individual: {target_file.name} ({lang.upper()})] ---")
    words_count = normalize_single_file(target_file, normalized_out)
    if words_count == 0:
        print(f"[Aviso] O arquivo '{target_file.name}' está vazio ou não possui palavras alfabéticas válidas.")
        return

    print(f"-> Palavras normalizadas: {words_count:,}")

    cmd = [str(SCANNER_BIN), lang, str(normalized_out), str(counts_out)]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"[Erro no scanner C]: {res.stderr}", file=sys.stderr)
        sys.exit(1)

    total_words, df = load_counts(counts_out)
    df_metrics = compute_metrics(df, total_words)
    print_report(total_words, df_metrics, f"{target_file.stem} ({lang})", top_n=15)
    plot_frequencies(df_metrics, f"{target_file.stem}", figure_out)
    print(f"[Concluído] Análise do arquivo concluída com sucesso!")

def run_normalization():
    print("\n--- [Etapa 1: Normalização (Python)] ---")
    words_pt = build_consolidated_corpus(RAW_PT_DIR, PROCESSED_PT_FILE)
    print(f"-> Corpus PT consolidado: {words_pt:,} palavras em {PROCESSED_PT_FILE}")

    words_en = build_consolidated_corpus(RAW_EN_DIR, PROCESSED_EN_FILE)
    print(f"-> Corpus EN consolidado: {words_en:,} palavras em {PROCESSED_EN_FILE}")

def run_scanning():
    print("\n--- [Etapa 2: Varredura por Janela Deslizante (C)] ---")
    compile_c_scanner_if_needed()

    # Scanner PT
    cmd_pt = [str(SCANNER_BIN), "pt", str(PROCESSED_PT_FILE), str(RESULTS_PT_FILE)]
    res_pt = subprocess.run(cmd_pt, capture_output=True, text=True)
    if res_pt.returncode != 0:
        print(f"[Erro no scanner PT]: {res_pt.stderr}", file=sys.stderr)
        sys.exit(1)
    print(res_pt.stdout.strip())

    # Scanner EN
    cmd_en = [str(SCANNER_BIN), "en", str(PROCESSED_EN_FILE), str(RESULTS_EN_FILE)]
    res_en = subprocess.run(cmd_en, capture_output=True, text=True)
    if res_en.returncode != 0:
        print(f"[Erro no scanner EN]: {res_en.stderr}", file=sys.stderr)
        sys.exit(1)
    print(res_en.stdout.strip())

def run_analytics():
    print("\n--- [Etapa 3: Análise Estatística e Visualização (Python)] ---")
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    # Análise PT
    if RESULTS_PT_FILE.exists():
        total_words_pt, df_pt = load_counts(RESULTS_PT_FILE)
        df_metrics_pt = compute_metrics(df_pt, total_words_pt)
        print_report(total_words_pt, df_metrics_pt, "Português", top_n=15)
        plot_frequencies(df_metrics_pt, "Português", OUT_DIR / "frequencias_pt.png")

    # Análise EN
    if RESULTS_EN_FILE.exists():
        total_words_en, df_en = load_counts(RESULTS_EN_FILE)
        df_metrics_en = compute_metrics(df_en, total_words_en)
        print_report(total_words_en, df_metrics_en, "Inglês", top_n=15)
        plot_frequencies(df_metrics_en, "Inglês", OUT_DIR / "frequencias_en.png")

    # Gráfico Comparativo
    if RESULTS_PT_FILE.exists() and RESULTS_EN_FILE.exists():
        generate_comparison_plot(df_metrics_pt, df_metrics_en, OUT_DIR / "comparativo_pt_en.png")

def main():
    parser = argparse.ArgumentParser(description="Pipeline de Análise e Criptoanálise de N-gramas (Python + C)")
    parser.add_argument("--step", choices=["all", "normalize", "scan", "analyze"], default="all",
                        help="Etapa a ser executada no corpus (padrão: all)")
    parser.add_argument("--file", type=str, default=None,
                        help="Caminho para analisar um único arquivo de texto individual")
    parser.add_argument("--lang", choices=["pt", "en"], default="pt",
                        help="Idioma do arquivo individual (pt ou en, padrão: pt)")
    args = parser.parse_args()

    # Se for passado um arquivo específico, roda a análise individual
    if args.file:
        analyze_single_file(Path(args.file), args.lang)
        return

    # Caso contrário, executa o fluxo padrão por corpus
    if args.step in ["all", "normalize"]:
        run_normalization()

    if args.step in ["all", "scan"]:
        run_scanning()

    if args.step in ["all", "analyze"]:
        run_analytics()

    print("\n[Sucesso] Execução do pipeline finalizada!")

if __name__ == "__main__":
    main()
