from flask import Flask, render_template, request
import pickle
import re

app = Flask(__name__)

vector = pickle.load(open("vectorizer.pkl", 'rb'))
model = pickle.load(open("phishing.pkl", 'rb'))

@app.route("/", methods=["GET", "POST"])
def index():

    predict = None   # IMPORTANT

    if request.method == "POST":

        url = request.form.get("url")

        if url:

            cleaned_url = re.sub(r'^https?://(www\.)?', '', url)

            result = model.predict(vector.transform([cleaned_url]))[0]

            print("Model output:", result)   # debug check

            if result == "bad" or result == 1:
                predict = "This is a Phishing website !!"
            elif result == "good" or result == 0:
                predict = "This is a healthy website !!"
            else:
                predict = "Unable to detect website"

    return render_template("index.html", predict=predict)


if __name__ == "__main__":
    app.run(debug=True)