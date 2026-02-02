# import numpy as np
import pandas as pd
import re
# import nltk
import pickle
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score, classification_report

df= pd.read_csv("reviews_badminton/data.csv")

df = df[["Review text", "Ratings"]]

df = df[df["Ratings"] != 3]

df["sentiment"] = df['Ratings'].apply(lambda x: 1 if x >= 4 else 0)

stop_words = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()

def clean_text(text):
    text = str(text).lower()
    text = re.sub(r"[^a-zA-Z]", " ", text)
    words = text.split()
    words = [lemmatizer.lemmatize(w) for w in words if w not in stop_words]
    return " ".join(words)

df["clean_review"] = df["Review text"].apply(clean_text)

X = df["clean_review"]
y = df["sentiment"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

tfidf = TfidfVectorizer(max_features=5000, ngram_range=(1,2))
X_train_vec = tfidf.fit_transform(X_train)
X_test_vec = tfidf.transform(X_test)

model = LogisticRegression(max_iter=1000)
model.fit(X_train_vec, y_train)

y_pred = model.predict(X_test_vec)
print("F1 Score:", f1_score(y_test, y_pred))
print(classification_report(y_test, y_pred))

pickle.dump(model, open("sentiment_model.pkl", "wb"))
pickle.dump(tfidf, open("tfidf.pkl", "wb"))

feature_names = tfidf.get_feature_names_out()
coefs = model.coef_[0]

negative_words = sorted(
    zip(feature_names, coefs),
    key=lambda x: x[1]
)[:20]

print("\nTop Negative Pain Points: ")
for word, coef in negative_words:
    print(word)