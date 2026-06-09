## Proebeln HA 3 MQM

# --- Kern (läuft auf dem Demo-Datensatz durch) ---
library(tidyverse)   # dplyr, ggplot2, stringr, tidyr
library(tidytext)    # unnest_tokens, bind_tf_idf, cast_dtm, tidy()
library(tokenizers)  # tokenize_words / tokenize_ngrams (im Kurs verwendet)
library(stopwords)   # stopwords(source="snowball", language="de")
library(SnowballC)   # wordStem(..., language="de")  -> Stemming
library(naivebayes)  # naive_bayes()  -> Klassifikation auf BoW (Kurs-Beispiel)
library(knitr)
library(dplyr)

# --- Optional, je nach gewählter Methode (einkommentieren) ---
# library(topicmodels) # LDA (Woche 13)
# library(textmineR)   # FitLdaModel + CalcProbCoherence (Kurs-Variante)
# library(word2vec)    # word2vec(), doc2vec() (Woche 12)
# library(reticulate)  # SBERT via Python sentence-transformers
# library(wordcloud)   # optionale Wordcloud


reviews <- read.csv("MQM_HA_3/twint_reviews_de.csv")







