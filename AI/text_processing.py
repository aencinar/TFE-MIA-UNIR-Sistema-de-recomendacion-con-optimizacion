import spacy
import re
import unicodedata
from unidecode import unidecode
from AI.words_map import words_map
from AI.words_map import extra_stopwords
from AI.words_map import protected_brands
from AI.words_map import protected_keywords
from AI.words_map import unidades_map

nlp = spacy.load("es_core_news_lg")


def normalize(text):
    return unicodedata.normalize('NFD', text).encode('ascii', 'ignore').decode("utf-8").lower()

def cleanUnicode(text: str) -> str:
    clean_text = unidecode(text)
    return clean_text


def preprocess_text(text: str) -> str:
    text_cleaned = re.sub(r"\(.*?\)", "", text)
    text_cleaned = re.sub(r"[^a-zA-Z0-9áéíóúñÁÉÍÓÚÑ\s]", "", text_cleaned)
    text_cleaned = text_cleaned.lower()

    for pattern, replacement in words_map.items():
        text_cleaned = re.sub(pattern, replacement, text_cleaned, flags=re.IGNORECASE)

    doc = nlp(text_cleaned)

    tokens = []
    protected_spans = set()
    norm_protected_brands = {normalize(b) for b in protected_brands}
    norm_protected_keywords = {normalize(k) for k in protected_keywords}

    for ent in doc.ents:
        if ent.label_ in {"ORG", "PRODUCT", "PER"}:
            for token in ent:
                protected_spans.add(token.i)

    for i, token in enumerate(doc):
        text_token = token.text.lower()
        lemma_token = token.lemma_.lower()
        text_norm = normalize(text_token)
        lemma_norm = normalize(lemma_token)

        if i in protected_spans:
            ent = next((e for e in doc.ents if e.start <= i < e.end), None)
            if ent and normalize(ent.text) in norm_protected_brands:
                tokens.append(ent.text)
                continue

        if text_norm in norm_protected_brands or lemma_norm in norm_protected_brands:
            tokens.append(token.text)
            continue

        if text_norm in norm_protected_keywords or lemma_norm in norm_protected_keywords:
            tokens.append(text_token)
            continue

        if (
            token.is_stop or
            text_token in extra_stopwords or
            lemma_token in extra_stopwords or
            token.is_punct or
            (len(text_token) < 2 and text_token not in protected_keywords)
        ):
            continue

        if token.like_num:
            tokens.append(text_token)
            continue

        if token.pos_ in ["NOUN", "ADJ", "PROPN"] and lemma_token not in {"granel", "pack"}:
            tokens.append(lemma_token)

    text_norm = normalize(text)
    for brand in protected_brands:
        brand_norm = normalize(brand)
        already_in_tokens = any(
            (brand_norm == normalize(t) or brand.upper() == t) for t in tokens
        )
        if brand_norm in text_norm and not already_in_tokens:
            tokens.insert(0, brand.upper())

    def deduplicate_brands(tokens):
        seen = set()
        result = []
        for t in tokens:
            if t.isupper() and t not in seen:
                seen.add(t)
                result.append(t)
            elif not t.isupper():
                result.append(t)
        return result

    tokens = deduplicate_brands(tokens)
    tokens = list(dict.fromkeys(tokens))

    clean_text = " ".join(tokens)
    clean_text = re.sub(r"\s+", " ", clean_text).strip()

    return clean_text if len(clean_text.split()) > 1 else text_cleaned.strip()




def process_text(text: str) -> str:
    p_text = cleanUnicode(text)
    p_text = preprocess_text(text)
    return p_text