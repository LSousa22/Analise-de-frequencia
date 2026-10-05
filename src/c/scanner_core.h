#ifndef SCANNER_CORE_H
#define SCANNER_CORE_H

#include <string.h>

/**
 * Conta o número de ocorrências de um padrão em uma palavra
 * utilizando janela deslizante com suporte a sobreposição (overlap).
 */
static inline int count_patterns_in_word(const char *word, const char *pattern) {
    if (!word || !pattern) return 0;
    int w_len = (int)strlen(word);
    int p_len = (int)strlen(pattern);
    if (w_len < p_len || p_len == 0) return 0;

    int count = 0;
    for (int i = 0; i <= w_len - p_len; i++) {
        if (strncmp(&word[i], pattern, (size_t)p_len) == 0) {
            count++;
        }
    }
    return count;
}

#endif /* SCANNER_CORE_H */
