import joblib
import re
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from flask import Flask, render_template, request

app = Flask(__name__)
model = joblib.load("../models/sentiment_model.pkl")
vectorizer = joblib.load("../models/tfidf_vectorizer.pkl")

stop_words = set(stopwords.words("english"))
stemmer = PorterStemmer()

def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z\s]', '', text)

    words = text.split()

    words = [
        stemmer.stem(word)
        for word in words
        if word not in stop_words
    ]

    return " ".join(words)

@app.route("/", methods=["GET", "POST"])
def home():

    prediction = None

    if request.method == "POST":

        review = request.form["review"]

        clean_review = preprocess_text(review)

        vector = vectorizer.transform([clean_review])

        prediction = model.predict(vector)[0]

    return render_template(
        "index.html",
        prediction=prediction
    )

if __name__ == "__main__":
    app.run(debug=True)