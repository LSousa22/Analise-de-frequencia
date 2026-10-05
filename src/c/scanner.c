#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include "dictionaries.h"
#include "scanner_core.h"

#define MAX_WORD_LEN 256
#define MAX_LINE_LEN 65536

/**
 * Processa uma única palavra do corpus:
 * incrementa a contagem de palavras e testa cada padrão de forma independente.
 */
static void process_word(const char *word, TargetPattern *patterns, int pattern_count) {
    if (!word || word[0] == '\0') return;
    for (int i = 0; i < pattern_count; i++) {
        int occurrences = count_patterns_in_word(word, patterns[i].pattern);
        patterns[i].count += occurrences;
    }
}

/**
 * Varre o arquivo de corpus consolidado.
 * Ignora linhas de cabeçalho/comentário iniciadas por '#'.
 */
int scan_corpus(const char *filepath, TargetPattern *patterns, int pattern_count, long *out_total_words) {
    FILE *fp = fopen(filepath, "r");
    if (!fp) {
        fprintf(stderr, "Erro: Não foi possível abrir o arquivo de entrada: %s\n", filepath);
        return 0;
    }

    char *line = (char *)malloc(MAX_LINE_LEN);
    if (!line) {
        fprintf(stderr, "Erro: Falha na alocação de memória para leitura de linha.\n");
        fclose(fp);
        return 0;
    }

    long total_words = 0;

    while (fgets(line, MAX_LINE_LEN, fp)) {
        /* Ignora linhas de comentários ou delimitadores de documento (# DOC: ...) */
        char *ptr = line;
        while (*ptr && isspace((unsigned char)*ptr)) ptr++;
        if (*ptr == '#' || *ptr == '\0') {
            continue;
        }

        /* Tokeniza a linha em palavras contíguas */
        char word[MAX_WORD_LEN];
        int w_idx = 0;

        while (*ptr) {
            if (isalpha((unsigned char)*ptr)) {
                if (w_idx < MAX_WORD_LEN - 1) {
                    word[w_idx++] = (char)tolower((unsigned char)*ptr);
                }
            } else {
                if (w_idx > 0) {
                    word[w_idx] = '\0';
                    total_words++;
                    process_word(word, patterns, pattern_count);
                    w_idx = 0;
                }
            }
            ptr++;
        }

        /* Última palavra da linha */
        if (w_idx > 0) {
            word[w_idx] = '\0';
            total_words++;
            process_word(word, patterns, pattern_count);
        }
    }

    free(line);
    fclose(fp);

    *out_total_words = total_words;
    return 1;
}

/**
 * Grava o resultado em CSV.
 * Formato: pattern,type,count
 */
int save_results_csv(const char *output_path, const TargetPattern *patterns, int pattern_count, long total_words) {
    FILE *fp = fopen(output_path, "w");
    if (!fp) {
        fprintf(stderr, "Erro: Não foi possível abrir o arquivo de saída para escrita: %s\n", output_path);
        return 0;
    }

    /* Linha de metadados: total_words */
    fprintf(fp, "# total_words,%ld\n", total_words);
    fprintf(fp, "pattern,type,count\n");

    for (int i = 0; i < pattern_count; i++) {
        fprintf(fp, "%s,%s,%ld\n", patterns[i].pattern, patterns[i].type, patterns[i].count);
    }

    fclose(fp);
    return 1;
}

int main(int argc, char *argv[]) {
    if (argc < 4) {
        printf("Uso: %s <pt|en> <input_corpus_path> <output_csv_path>\n", argv[0]);
        printf("Exemplo: %s pt data/processed/corpus_pt.txt data/results/counts_pt.csv\n", argv[0]);
        return 1;
    }

    const char *lang = argv[1];
    const char *input_path = argv[2];
    const char *output_path = argv[3];

    TargetPattern *patterns = NULL;
    int pattern_count = 0;

    if (strcmp(lang, "pt") == 0 || strcmp(lang, "pt-br") == 0) {
        patterns = PT_PATTERNS;
        pattern_count = PT_PATTERNS_COUNT;
    } else if (strcmp(lang, "en") == 0 || strcmp(lang, "eng") == 0) {
        patterns = EN_PATTERNS;
        pattern_count = EN_PATTERNS_COUNT;
    } else {
        fprintf(stderr, "Erro: Idioma desconhecido '%s'. Utilize 'pt' ou 'en'.\n", lang);
        return 1;
    }

    printf("Iniciando varredura (%s)...\n", lang);
    printf("Arquivo de entrada: %s\n", input_path);

    long total_words = 0;
    if (!scan_corpus(input_path, patterns, pattern_count, &total_words)) {
        return 1;
    }

    if (!save_results_csv(output_path, patterns, pattern_count, total_words)) {
        return 1;
    }

    printf("Varredura concluida com sucesso!\n");
    printf("- Total de palavras analisadas: %ld\n", total_words);
    printf("- Padroes avaliados: %d\n", pattern_count);
    printf("- Resultados salvos em: %s\n", output_path);

    return 0;
}
