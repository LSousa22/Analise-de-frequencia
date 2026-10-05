# Cripto - Varredura e Análise de N-Gramas (Python + C)

Sistema para análise de frequência de digramas e trigramas em textos em Português e Inglês, produzido para a disciplina de Tópicos especiais em engenharia de software (Criptografia).

---

## Arquitetura do Sistema

O sistema opera em um pipeline em 3 estágios independentes baseados em arquivos:

Texto Brutos -> texto normalizado -> frequencias brutas -> métricas gráficas e via cli
---

## 📂 Estrutura de Pastas

```text
Cripto/
├── bin/                           # Executáveis compilados (scanner.exe)
├── data/
│   ├── raw/                       # Adicione seus textos .txt aqui
│   │   ├── pt-br/                 # Textos em português
│   │   └── eng/                   # Textos em inglês
│   ├── processed/                 # Textos normalizados consolidados (gerados pelo normalizer)
│   │   ├── corpus_pt.txt
│   │   └── corpus_en.txt
│   └── results/                   # Saídas brutas geradas pelo scanner em C
│       ├── counts_pt.csv
│       └── counts_en.csv
│
├── docs/                          # Documentações e tabelas de referência
│   ├── di-trigrams.md             # Tabela de referência de digramas e trigramas
│   └── sample-texts.md            # Textos de exemplo e referências
│
├── out/                           # Gráficos de barras e comparativos salvos em PNG
├── src/
│   ├── python/
│   │   ├── normalizer.py          # Etapa 1: Limpeza Unicode NFKD, remoção de acentos e regex [a-z]
│   │   ├── analytics.py           # Etapa 3: Cálculo de métricas e geração de gráficos com Matplotlib
│   │   └── config.py              # Definições de caminhos e constantes do projeto
│   └── c/
│       ├── scanner.c              # Etapa 2: Motor C com janela deslizante e contagem com overlap
│       ├── scanner_core.h         # Lógica central e headers de leitura e contagem de n-gramas
│       ├── dictionaries.h         # Dicionários de digramas e trigramas embutidos
│       └── Makefile               # Regras de compilação via GCC
│
├── tests/                         # Suíte de testes unitários e de integração
│   ├── test_normalizer.py
│   ├── test_scanner.c
│   ├── test_scanner_e2e.py
│   └── test_analytics.py
│
├── main.py                        # Orquestrador mestre (executa todo o pipeline ou arquivo individual)
├── requirements.txt               # Dependências Python (pandas, matplotlib)
└── README.md                      # Documentação do projeto
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

### 3. Executar com um Arquivo Específico
Para analisar um único arquivo de texto de forma isolada, gerando o relatório no terminal e o gráfico individual salvo em `out/`:

```bash
# Para texto em português (padrão):
python main.py --file caminho/do/arquivo.txt

# Ou especificando explicitamente o idioma (pt ou en):
python main.py --file caminho/do/arquivo.txt --lang pt
python main.py --file caminho/do/arquivo.txt --lang en
```

### 4. Executar Etapas Isoladas
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
