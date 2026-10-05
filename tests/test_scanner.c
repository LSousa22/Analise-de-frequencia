#include <stdio.h>
#include <assert.h>
#include "../src/c/scanner_core.h"

int main(void) {
    printf("Iniciando testes unitários do scanner em C...\n");

    /* Caso 1: Palavra menor que o padrão */
    assert(count_patterns_in_word("a", "aa") == 0);

    /* Caso 2: Padrão inexistente */
    assert(count_patterns_in_word("casa", "er") == 0);

    /* Caso 3: Ocorrência simples */
    assert(count_patterns_in_word("queijo", "qu") == 1);
    assert(count_patterns_in_word("queijo", "que") == 1);

    /* Caso 4: Múltiplas ocorrências sem sobreposição */
    assert(count_patterns_in_word("banana", "an") == 2);

    /* Caso 5: Sobreposição obrigatória (Overlap) especificada na regra */
    /* Ex.: "aa" em "aaa" -> deve contar exatamente 2 */
    assert(count_patterns_in_word("aaa", "aa") == 2);

    /* Ex.: "aa" em "aaaa" -> deve contar 3 */
    assert(count_patterns_in_word("aaaa", "aa") == 3);

    /* Caso 6: Palavra vazia ou ponteiro nulo */
    assert(count_patterns_in_word("", "a") == 0);
    assert(count_patterns_in_word(NULL, "a") == 0);
    assert(count_patterns_in_word("a", NULL) == 0);

    printf("Todos os testes do scanner em C passaram com sucesso!\n");
    return 0;
}
