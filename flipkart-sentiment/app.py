from flask import Flask, render_template, request
import pickle
import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

app = Flask(__name__)

model = pickle.load(open("sentiment_model.pkl", "rb"))
tfidf = pickle.load(open("tfidf.pkl", "rb"))

stop_words = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()

def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^a-zA-Z]", " ", text)
    words = text.split()
    words = [lemmatizer.lemmatize(w) for w in words if w not in stop_words]
    return " ".join(words)

@app.route("/", methods=["GET", "POST"])
def index():
    sentiment = None
    review = ""

    if request.method == "POST":
        review = request.form["review"]
        cleaned = clean_text(review)
        vector = tfidf.transform([cleaned])
        prediction = model.predict(vector)[0]
        sentiment = "Positive 😊" if prediction == 1 else "Negative 😠"

    return render_template("index.html", sentiment=sentiment, review=review)

import mlflow.pyfunc

model = mlflow.pyfunc.load_model(
    "models:/FlipkartSentimentModel/Production"
)

if __name__ == "__main__":
    app.run(debug=True)
