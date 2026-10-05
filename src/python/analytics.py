import os
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

def load_counts(csv_path: Path) -> tuple[int, pd.DataFrame]:
    """
    Lê o CSV gerado pelo scanner C.
    Extrai o número total de palavras gravado no cabeçalho (# total_words,N)
    e carrega as linhas de dados em um DataFrame.
    """
    csv_file = Path(csv_path)
    total_words = 0

    with open(csv_file, "r", encoding="utf-8") as f:
        first_line = f.readline().strip()
        if first_line.startswith("# total_words,"):
            total_words = int(first_line.split(",")[1])

    # Lê o CSV ignorando linhas comentadas
    df = pd.read_csv(csv_file, comment="#")
    return total_words, df

def compute_metrics(df: pd.DataFrame, total_words: int) -> pd.DataFrame:
    """
    Calcula:
    - Frequência relativa (count / total_words)
    - Frequência por 1.000 palavras ((count / total_words) * 1000)
    - Ranking ordenado do maior para o menor
    """
    df = df.copy()
    if total_words > 0:
        df["relative_frequency"] = df["count"] / total_words
        df["freq_per_1000"] = (df["count"] / total_words) * 1000.0
    else:
        df["relative_frequency"] = 0.0
        df["freq_per_1000"] = 0.0

    df = df.sort_values(by="count", ascending=False).reset_index(drop=True)
    df["rank"] = df.index + 1
    return df

def print_report(total_words: int, df_metrics: pd.DataFrame, lang_label: str, top_n: int = 15) -> None:
    """
    Exibe no terminal o relatório formatado exigido pela especificação.
    """
    print("\n" + "=" * 65)
    print(f" RELATÓRIO DE VARREDURA DE N-GRAMAS - IDIOMA: {lang_label.upper()}")
    print("=" * 65)
    print(f" Total de palavras analisadas no corpus: {total_words:,}")
    print(f" Total de padrões avaliados: {len(df_metrics)}")
    print("-" * 65)
    print(f"{'Rank':<5} {'Padrão':<8} {'Tipo':<10} {'Freq. Absoluta':<16} {'Freq. Relativa':<15} {'Por 1.000 pal.'}")
    print("-" * 65)

    display_df = df_metrics.head(top_n)
    for _, row in display_df.iterrows():
        print(f"{int(row['rank']):<5} "
              f"{row['pattern']:<8} "
              f"{row['type']:<10} "
              f"{int(row['count']):<16} "
              f"{row['relative_frequency']:<15.6f} "
              f"{row['freq_per_1000']:<10.2f}")
    print("=" * 65)

def plot_frequencies(df_metrics: pd.DataFrame, lang_label: str, output_image: Path, top_n: int = 12) -> None:
    """
    Gera gráfico de barras com os digramas e trigramas mais frequentes.
    Salva a imagem em alta resolução.
    """
    output_path = Path(output_image)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    digrams = df_metrics[df_metrics["type"] == "digrama"].head(top_n)
    trigrams = df_metrics[df_metrics["type"] == "trigrama"].head(top_n)

    fig, axes = plt.subplots(1, 2, figsize=(14, 6), sharey=False)

    # Gráfico de Digramas
    axes[0].bar(digrams["pattern"], digrams["count"], color="#2b5c8f", edgecolor="black")
    axes[0].set_title(f"Top {top_n} Digramas ({lang_label.upper()})", fontsize=13, fontweight="bold")
    axes[0].set_xlabel("Digrama", fontsize=11)
    axes[0].set_ylabel("Frequência Absoluta", fontsize=11)
    axes[0].grid(axis="y", linestyle="--", alpha=0.7)

    # Gráfico de Trigramas
    axes[1].bar(trigrams["pattern"], trigrams["count"], color="#d95f02", edgecolor="black")
    axes[1].set_title(f"Top {top_n} Trigramas ({lang_label.upper()})", fontsize=13, fontweight="bold")
    axes[1].set_xlabel("Trigrama", fontsize=11)
    axes[1].set_ylabel("Frequência Absoluta", fontsize=11)
    axes[1].grid(axis="y", linestyle="--", alpha=0.7)

    plt.suptitle(f"Frequência de Caracteres e N-gramas - Corpus {lang_label.upper()}", fontsize=15, fontweight="bold")
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f"-> Gráfico salvo com sucesso em: {output_path}")

def generate_comparison_plot(df_pt: pd.DataFrame, df_en: pd.DataFrame, output_image: Path, top_n: int = 10) -> None:
    """
    Gera um gráfico comparativo de digramas mais frequentes entre Português e Inglês.
    """
    output_path = Path(output_image)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    pt_top = df_pt[df_pt["type"] == "digrama"].head(top_n).copy()
    en_top = df_en[df_en["type"] == "digrama"].head(top_n).copy()

    fig, axes = plt.subplots(2, 1, figsize=(12, 8))

    axes[0].bar(pt_top["pattern"], pt_top["freq_per_1000"], color="#2b5c8f")
    axes[0].set_title(f"Top {top_n} Digramas no Português (Taxa por 1.000 palavras)", fontsize=12, fontweight="bold")
    axes[0].set_ylabel("Freq. por 1.000 pal.")
    axes[0].grid(axis="y", linestyle="--", alpha=0.7)

    axes[1].bar(en_top["pattern"], en_top["freq_per_1000"], color="#1b9e77")
    axes[1].set_title(f"Top {top_n} Digramas no Inglês (Taxa por 1.000 palavras)", fontsize=12, fontweight="bold")
    axes[1].set_ylabel("Freq. por 1.000 pal.")
    axes[1].grid(axis="y", linestyle="--", alpha=0.7)

    plt.suptitle("Comparativo de Frequência de Digramas: Português vs Inglês", fontsize=14, fontweight="bold")
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f"-> Gráfico comparativo salvo em: {output_path}")
