#ifndef DICTIONARIES_H
#define DICTIONARIES_H

typedef struct {
    const char *pattern;
    const char *type; /* "digrama" ou "trigrama" */
    long count;
} TargetPattern;

/* Dicionário de Português (30 digramas + 30 trigramas) conforme di-trigrams.md */
static TargetPattern PT_PATTERNS[] = {
    /* Digramas */
    {"de", "digrama", 0}, {"en", "digrama", 0}, {"er", "digrama", 0},
    {"te", "digrama", 0}, {"es", "digrama", 0}, {"as", "digrama", 0},
    {"re", "digrama", 0}, {"os", "digrama", 0}, {"da", "digrama", 0},
    {"em", "digrama", 0}, {"do", "digrama", 0}, {"qu", "digrama", 0},
    {"nt", "digrama", 0}, {"co", "digrama", 0}, {"or", "digrama", 0},
    {"ar", "digrama", 0}, {"ra", "digrama", 0}, {"ia", "digrama", 0},
    {"al", "digrama", 0}, {"an", "digrama", 0}, {"st", "digrama", 0},
    {"ta", "digrama", 0}, {"ca", "digrama", 0}, {"ti", "digrama", 0},
    {"ro", "digrama", 0}, {"me", "digrama", 0}, {"ma", "digrama", 0},
    {"nd", "digrama", 0}, {"ci", "digrama", 0}, {"pr", "digrama", 0},

    /* Trigramas (com "TÃO" normalizado para "tao") */
    {"que", "trigrama", 0}, {"ent", "trigrama", 0}, {"con", "trigrama", 0},
    {"est", "trigrama", 0}, {"nto", "trigrama", 0}, {"ado", "trigrama", 0},
    {"ndo", "trigrama", 0}, {"men", "trigrama", 0}, {"res", "trigrama", 0},
    {"com", "trigrama", 0}, {"par", "trigrama", 0}, {"ter", "trigrama", 0},
    {"pre", "trigrama", 0}, {"ica", "trigrama", 0}, {"ara", "trigrama", 0},
    {"tra", "trigrama", 0}, {"ste", "trigrama", 0}, {"pro", "trigrama", 0},
    {"ete", "trigrama", 0}, {"tao", "trigrama", 0}, {"and", "trigrama", 0},
    {"sta", "trigrama", 0}, {"mpo", "trigrama", 0}, {"aca", "trigrama", 0},
    {"rme", "trigrama", 0}, {"tad", "trigrama", 0}, {"odo", "trigrama", 0},
    {"ode", "trigrama", 0}, {"lha", "trigrama", 0}, {"des", "trigrama", 0}
};
static const int PT_PATTERNS_COUNT = sizeof(PT_PATTERNS) / sizeof(PT_PATTERNS[0]);

/* Dicionário de Inglês (30 digramas + 30 trigramas) conforme di-trigrams.md */
static TargetPattern EN_PATTERNS[] = {
    /* Digramas */
    {"th", "digrama", 0}, {"he", "digrama", 0}, {"in", "digrama", 0},
    {"er", "digrama", 0}, {"an", "digrama", 0}, {"re", "digrama", 0},
    {"on", "digrama", 0}, {"at", "digrama", 0}, {"en", "digrama", 0},
    {"nd", "digrama", 0}, {"ti", "digrama", 0}, {"es", "digrama", 0},
    {"or", "digrama", 0}, {"te", "digrama", 0}, {"of", "digrama", 0},
    {"ed", "digrama", 0}, {"is", "digrama", 0}, {"it", "digrama", 0},
    {"al", "digrama", 0}, {"ar", "digrama", 0}, {"st", "digrama", 0},
    {"to", "digrama", 0}, {"nt", "digrama", 0}, {"ng", "digrama", 0},
    {"se", "digrama", 0}, {"ha", "digrama", 0}, {"as", "digrama", 0},
    {"ou", "digrama", 0}, {"io", "digrama", 0}, {"le", "digrama", 0},

    /* Trigramas */
    {"the", "trigrama", 0}, {"and", "trigrama", 0}, {"ing", "trigrama", 0},
    {"ent", "trigrama", 0}, {"ion", "trigrama", 0}, {"her", "trigrama", 0},
    {"for", "trigrama", 0}, {"tha", "trigrama", 0}, {"nth", "trigrama", 0},
    {"int", "trigrama", 0}, {"ere", "trigrama", 0}, {"tio", "trigrama", 0},
    {"ter", "trigrama", 0}, {"est", "trigrama", 0}, {"ers", "trigrama", 0},
    {"ati", "trigrama", 0}, {"hat", "trigrama", 0}, {"ate", "trigrama", 0},
    {"all", "trigrama", 0}, {"eth", "trigrama", 0}, {"hes", "trigrama", 0},
    {"ver", "trigrama", 0}, {"his", "trigrama", 0}, {"oft", "trigrama", 0},
    {"ith", "trigrama", 0}, {"fth", "trigrama", 0}, {"sth", "trigrama", 0},
    {"nce", "trigrama", 0}, {"con", "trigrama", 0}, {"res", "trigrama", 0}
};
static const int EN_PATTERNS_COUNT = sizeof(EN_PATTERNS) / sizeof(EN_PATTERNS[0]);

#endif /* DICTIONARIES_H */
