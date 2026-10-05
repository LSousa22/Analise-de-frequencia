# Cripto - Varredura e Análise de N-Gramas (Python + C)

Sistema híbrido de alto desempenho para análise de frequência de digramas e trigramas em textos em Português e Inglês. Combina a facilidade e robustez do Python para normalização de texto e análise estatística/gráfica com a velocidade do C para varredura com janela deslizante e contagem de padrões com sobreposição (*overlap*).

---

## 🏛 Arquitetura do Sistema

O sistema opera em um pipeline desacoplado em 3 estágios independentes baseados em arquivos:

```text
[Textos Brutos em data/raw/{pt-br,eng}]
       ↓ (Etapa 1 - Python: normalizer.py)
[Corpus Normalizado em data/processed/corpus_{pt,en}.txt]
       ↓ (Etapa 2 - C: bin/scanner.exe)
[Frequências Brutas em data/results/counts_{pt,en}.csv]
       ↓ (Etapa 3 - Python: analytics.py)
[Tabelas de Métricas no Terminal & Gráficos em out/]
```

---

## 📂 Estrutura de Pastas

```text
Cripto/
├── data/
│   ├── raw/                       # Adicione seus textos .txt aqui
│   │   ├── pt-br/                 # ~20 textos em português
│   │   └── eng/                   # ~20 textos em inglês
│   ├── processed/                 # Textos normalizados consolidados (gerados pelo normalizer)
│   │   ├── corpus_pt.txt
│   │   └── corpus_en.txt
│   └── results/                   # Saídas brutas geradas pelo scanner em C
│       ├── counts_pt.csv
│       └── counts_en.csv
│
├── src/
│   ├── python/
│   │   ├── normalizer.py          # Etapa 1: Limpeza Unicode NFKD, remoção de acentos e regex [a-z]
│   │   ├── analytics.py           # Etapa 3: Cálculo de métricas e geração de gráficos com Matplotlib
│   │   └── config.py              # Definições de caminhos e constantes do projeto
│   └── c/
│       ├── scanner.c              # Etapa 2: Motor C com janela deslizante e contagem com overlap
│       ├── dictionaries.h         # Dicionários de digramas e trigramas embutidos (di-trigrams.md)
│       └── Makefile               # Regras de compilação via GCC
│
├── bin/                           # Executáveis compilados (scanner.exe)
├── out/                           # Gráficos de barras e comparativos salvos em PNG
├── tests/                         # Suíte de testes unitários e de integração
├── docs/
│   └── GLOSSARY.md                # Glossário de termos e regras canônicas do domínio
│
├── main.py                        # Orquestrador mestre (executa todo o pipeline)
├── requirements.txt               # Dependências Python (pandas, matplotlib)
├── di-trigrams.md                 # Tabela de referência de digramas e trigramas
└── visao.md                       # Especificação original do projeto
```

---

## 🚀 Como Executar

### 1. Pré-requisitos
- **Python 3.10+** (com `pandas` e `matplotlib` instalados)
- **GCC** (MinGW / w64devkit no Windows ou GCC padrão no Linux)

Instale as dependências Python se necessário:
```bash
pip install -r requirements.txt
```

### 2. Executar o Pipeline Completo
Para rodar todas as etapas de ponta a ponta (normalização $\rightarrow$ compilação/varredura C $\rightarrow$ relatórios e gráficos):
```bash
python main.py
```

### 3. Executar Etapas Isoladas
Você pode rodar qualquer etapa de forma independente:
- **Apenas normalizar os textos:**
  ```bash
  python main.py --step normalize
  # ou diretamente:
  python src/python/normalizer.py
  ```
- **Apenas rodar o scanner em C:**
  ```bash
  python main.py --step scan
  # ou diretamente via linha de comando:
  gcc -O3 src/c/scanner.c -o bin/scanner.exe
  ./bin/scanner.exe pt data/processed/corpus_pt.txt data/results/counts_pt.csv
  ```
- **Apenas gerar análises e gráficos:**
  ```bash
  python main.py --step analyze
  ```

---

## 🧪 Suíte de Testes

Para executar todos os testes automatizados (Python e C):
```bash
python -m unittest discover -s tests -p "test_*.py"
gcc tests/test_scanner.c -o bin/test_scanner.exe && ./bin/test_scanner.exe
```

---

## 📊 Regras de Negócio Implementadas

1. **Normalização Rígida**: Decomposição Unicode NFKD, conversão para minúsculas, remoção integral de acentos/diacríticos e isolamento estrito de caracteres `[a-z]+`.
2. **Fronteira de Palavra (Word Boundary)**: O scanner opera estritamente palavra por palavra; nenhum n-grama cruza limites entre palavras contíguas.
3. **Sobreposição (Overlap)**: Ocorrências contíguas compartilhadas são detectadas via janela deslizante (ex.: `aa` em `aaa` resulta em 2 ocorrências).
4. **Métricas**: Frequência absoluta, frequência relativa ($\frac{\text{ocorrências}}{\text{total de palavras}}$) e frequência ponderada por 1.000 palavras.
