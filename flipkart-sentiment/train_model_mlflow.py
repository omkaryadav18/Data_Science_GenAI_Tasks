import pandas as pd
import re
import pickle
import mlflow
import mlflow.sklearn
import matplotlib.pyplot as plt

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score, classification_report

# ---------------------------
# MLflow setup
# ---------------------------
mlflow.set_experiment("Flipkart_Sentiment_Analysis")

# ---------------------------
# Load data
# ---------------------------
df = pd.read_csv("reviews_badminton/data.csv")
df = df[["Review text", "Ratings"]]
df = df[df["Ratings"] != 3]
df["sentiment"] = df["Ratings"].apply(lambda x: 1 if x >= 4 else 0)

# ---------------------------
# Text preprocessing
# ---------------------------
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

# ---------------------------
# Train-test split
# ---------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# ---------------------------
# Hyperparameters
# ---------------------------
tfidf_max_features = 5000
ngram_range = (1, 2)
max_iter = 1000

# ---------------------------
# MLflow run
# ---------------------------
with mlflow.start_run(run_name="LogReg_TFIDF_v1"):

    # TF-IDF
    tfidf = TfidfVectorizer(
        max_features=tfidf_max_features,
        ngram_range=ngram_range
    )
    X_train_vec = tfidf.fit_transform(X_train)
    X_test_vec = tfidf.transform(X_test)

    # Model
    model = LogisticRegression(max_iter=max_iter)
    model.fit(X_train_vec, y_train)

    # Predictions
    y_pred = model.predict(X_test_vec)

    # Metrics
    f1 = f1_score(y_test, y_pred)

    print("F1 Score:", f1)
    print(classification_report(y_test, y_pred))

    # ---------------------------
    # MLflow logging
    # ---------------------------
    mlflow.log_param("model", "LogisticRegression")
    mlflow.log_param("tfidf_max_features", tfidf_max_features)
    mlflow.log_param("ngram_range", str(ngram_range))
    mlflow.log_param("max_iter", max_iter)

    mlflow.log_metric("f1_score", f1)

    # ---------------------------
    # Save artifacts
    # ---------------------------
    pickle.dump(model, open("sentiment_model.pkl", "wb"))
    pickle.dump(tfidf, open("tfidf.pkl", "wb"))

    mlflow.log_artifact("sentiment_model.pkl")
    mlflow.log_artifact("tfidf.pkl")

    # ---------------------------
    # Register model (optional but recommended)
    # ---------------------------
    mlflow.sklearn.log_model(
        model,
        artifact_path="model",
        registered_model_name="FlipkartSentimentModel"
    )

# ---------------------------
# Pain point extraction (same as before)
# ---------------------------
feature_names = tfidf.get_feature_names_out()
coefs = model.coef_[0]

negative_words = sorted(
    zip(feature_names, coefs),
    key=lambda x: x[1]
)[:20]

print("\nTop Negative Pain Points:")
for word, coef in negative_words:
    print(word)

 #Sentiment Distribution
df["sentiment"].value_counts().plot(
    kind="bar",
    color=["#4CAF50", "#F44336"]
)
plt.xticks([0,1], ["Positive", "Negative"], rotation=0)
plt.title("Sentiment Distribution of Reviews")
plt.ylabel("Number of Reviews")
plt.show()

#Rating vs Sentiment Mapping
df["sentiment"].value_counts().plot(
    kind="bar",
    color=["#4CAF50", "#F44336"]
)
plt.xticks([0,1], ["Positive", "Negative"], rotation=0)
plt.title("Sentiment Distribution of Reviews")
plt.ylabel("Number of Reviews")
plt.show()

#Top Negative Pain Points
neg_words_df = pd.DataFrame(negative_words, columns=["Word", "Coefficient"])

plt.figure(figsize=(8,5))
plt.barh(neg_words_df["Word"], neg_words_df["Coefficient"])
plt.title("Top Negative Customer Pain Points")
plt.gca().invert_yaxis()
plt.show()