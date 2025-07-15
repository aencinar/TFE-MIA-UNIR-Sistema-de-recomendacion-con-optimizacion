extra_stopwords = {
    "alcampo", "mercadona", "eroski", "extra", "bolsa", "peso", "aproximado", "envase",
    "bote", "tarro", "a granel", "bandeja", "lata", "botella", "maduro", "madura", "producto"
}

protected_brands = {
    "tarradellas", "hacendado", "coca-cola", "barceló", "amstel",
    "heineken", "danone", "gullón", "gullon", "nestlé", "orígens",
    "origens", "beefeater", "pescanova", "selecciona",
    "auchan", "bueno", "gallo", "nestlé", "kaiku","carretilla",
    "campofrío", "oetker", "helios", "el pozo", "lindt", "frit ravich",
    "milka", "pedro luis", "don simon", "calvo","gourmet", "igp",
    "findus", "albo", "puleva", "ducros", "haribo", "la lechera",
    "gallina blanca", "central lechera asturiana", "ybarra", "carmencita",
    "granini", "pascual", "borges", "juver", "luengo", "casa tarradellas",
    "cocinera", "royal", "navidul", "coren", "dulcesol", "miguelañez",
    "kellogg", "old el paso", "tulipán", "prima", "príncipe", "mercader",
    "musa", "pompadour", "amatista", "gvtarra", "martini", "artiach",
    "viña albali", "mahou", "marqués", "freixenet","cune", "codorniu",
    "casera", "font vella", "fanta", "monster", "aquarius","kas", "coto",
    "estrella galicia", "yosoy", "cruzcampo", "castillo", "alpro", "bach",
    "top lider", "bezolla", "maggi", "serpis", "delfín","harimsa", "yatekomo",
    "argal", "sal costa", "el tigre", "litoral", "palacios", "maxifoods", "cornetto",
    "la asturiana","la española","dolce gusto", "la cocinera"
}

protected_keywords = {
    "ron", "margarita", "pizza", "platano", "vino", "boqueron", "g", "kg", "ml", "l", "cl", "unidad", "unidades", "pack"
}

words_map = {
    r"(\d+)[ ]?(gr|gramos?|g\.?)\b": r"\1g",
    r"(\d+)[ ]?(kg|kilos?|kg\.?)\b": r"\1kg",
    r"(\d+)[ ]?(ml|mililitros?|cc)\b": r"\1ml",
    r"(\d+)[ ]?(l|litros?|lt|lts)\b": r"\1l",
    r"(\d+)[ ]?cl\b": r"\1cl",
    r"\b(plátanos?|bananas?)\b": "platano",
    r"\b(de comercio justo|maduros?|CULTIVAMOS LO BUENO|IGP|Indicación Geográfica Protegida)\b": "",
    r"\b(ecológicas?|bio|organic)\b": "ecologico",
    r"\b(pz|ud|uds)\b": "unidad",                       # "ud", "uds", "pz" → "unidad"
    r"\bx[\s\-]?(\d+)\b": r"\1 unidades",               # "x6", "x 12", "x-4" → "6 unidades", "12 unidades", "4 unidades"
    r"\b(\d+)\s*(uds?|unidades?)\b": r"\1 unidades",    # "6 uds", "6 unidades" → "6 unidades"
    r"\b(\d+)\s*pack\b": r"\1 pack",
    r"\bgarbanzo cocido\b": "garbanzo",
    r"\balubia roja\b": "alubia",
    r"\blentejas pardinas\b": "lenteja",
    r"\bplátanir\b": "platano",
    r"\bcervezas\b": "cerveza",
    r"\b\d+[,.]\d+%?\b": "",
    r"\b(a granel|bandeja|malla|barqueta)\b": "",
    r"(\d+)\s*(gr?|gramos?)(\b|$)": r"\1g",
    r"\bpara freir\b": "fritura",
    r"\bde zumo\b": "zumo",
}

unidades_map = {
    "gr": "g",
    "gramo": "g",
    "gramos": "g",
    "kg": "kg",
    "kilo": "kg",
    "kilos": "kg",
    "ml": "ml",
    "mililitros": "ml",
    "l": "l",
    "litro": "l",
    "litros": "l",
    "cl": "cl",
    "cc": "ml",
    "g.": "g",
    "kg.": "kg",
    "lt": "l",
    "lts": "l",
}
