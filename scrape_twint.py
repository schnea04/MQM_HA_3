"""
scrape_twint.py -- Google-Play-Reviews der TWINT-App ziehen (MqM HA3).
Einmal ausfuehren  ->  erzeugt twint_reviews.csv (danach Analyse in R).

Setup:  pip install google-play-scraper pandas
"""

from google_play_scraper import Sort, reviews_all
import pandas as pd

# App-ID = der "id=..."-Teil der Play-Store-URL.
# "ch.twint.payment" = generische "Prepaid TWINT & other banks"-App.
# Mehrere Apps kombinieren? Liste erweitern, dann wird eine Spalte "app" angelegt.
APP_IDS = {
    "UBS TWINT": "com.ubs.Paymit.android",
    # "PostFinance TWINT": "ch.postfinance.twint.android",
}

frames = []
for app_name, app_id in APP_IDS.items():
    rev = reviews_all(
        app_id,
        lang="de",            # Antwort-Sprache
        country="ch",         # Markt Schweiz
        sort=Sort.NEWEST,
        sleep_milliseconds=200,  # hoeflich bleiben, Server nicht hammern
    )
    d = pd.DataFrame(rev)
    d["app"] = app_name
    frames.append(d)

df = pd.concat(frames, ignore_index=True)

# Nur die relevanten Spalten; Usernamen bewusst NICHT uebernehmen (Datenschutz).
df = df[["app", "content", "score", "at", "thumbsUpCount", "reviewCreatedVersion"]]
df = df.rename(columns={"content": "text", "score": "rating", "at": "date"})

# Aufraeumen: leere/sehr kurze Reviews raus, Duplikate raus (vgl. W11, S.51).
df = df.dropna(subset=["text"])
df = df[df["text"].str.len() >= 20]
df = df.drop_duplicates(subset=["text"]).reset_index(drop=True)
df.insert(0, "doc_id", range(1, len(df) + 1))

df.to_csv("twint_reviews.csv", index=False, encoding="utf-8")

print(f"{len(df)} Reviews gespeichert -> twint_reviews.csv")
print("\nRating-Verteilung:")
print(df["rating"].value_counts().sort_index())
