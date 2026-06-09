"""
translate_reviews.py -- Nicht-deutsche TWINT-Reviews auf Deutsch uebersetzen (MqM HA3).
Einmal ausfuehren  ->  twint_reviews_de.csv  (danach Analyse in R auf Spalte text_de).
WICHTIG: NICHT im .Rmd bei jedem Knit uebersetzen -> einmal cachen.

Setup:  pip install deep-translator langdetect pandas
"""

import time
import pandas as pd
from langdetect import detect_langs, LangDetectException
from deep_translator import GoogleTranslator

df = pd.read_csv("twint_reviews.csv")


def erkenne_sprache(t):
    """Wahrscheinlichste Sprache; bei kurzen/unsicheren Texten None."""
    if not isinstance(t, str) or len(t.strip()) < 3:
        return None
    try:
        top = detect_langs(t)[0]                 # Sprache + Wahrscheinlichkeit
        return top.lang if top.prob >= 0.90 else None
    except LangDetectException:
        return None


df["lang"] = df["text"].apply(erkenne_sprache)

uebersetzer = GoogleTranslator(source="auto", target="de")


def nach_deutsch(row):
    t, lang = row["text"], row["lang"]
    if not isinstance(t, str) or lang in (None, "de"):
        return t                                 # Deutsch oder unsicher -> Original behalten
    try:
        time.sleep(0.2)                          # hoeflich bleiben
        return uebersetzer.translate(t[:4900])   # Google-Limit ~5000 Zeichen pro Call
    except Exception:
        return t                                 # bei Fehler Original behalten


df["text_de"] = df.apply(nach_deutsch, axis=1)

df.to_csv("twint_reviews_de.csv", index=False, encoding="utf-8")

print("Erkannte Sprachen:")
print(df["lang"].value_counts(dropna=False))
print(f"\nUebersetzt: {(df['lang'].notna() & (df['lang'] != 'de')).sum()} Reviews")
print("Gespeichert -> twint_reviews_de.csv")
