from flask import Flask, render_template, request
from dotenv import load_dotenv
import requests
import os

load_dotenv()

app = Flask(__name__)

api_key = os.getenv("OMDB_API_KEY")

def format_votes(votes):
    votes = int(votes.replace(",", ""))

    if votes >= 1_000_000:
        value = f"{votes / 1_000_000:.1f}".rstrip("0").rstrip(".")
        return f"{value}M"

    elif votes >= 1_000:
        value = f"{votes / 1_000:.1f}".rstrip("0").rstrip(".")
        return f"{value}K"

    return str(votes)

@app.route("/", methods=["GET", "POST"])
def home():

    movie = None

    if request.method == "POST":

        movie_name = request.form.get("movie", "").strip()

        url = f"http://www.omdbapi.com/?t={movie_name}&apikey={api_key}"

        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()

            data = response.json()

            if data["Response"] == "True":
                data["formatted_votes"] = format_votes(data["imdbVotes"])
                movie = data

        except requests.RequestException:
            pass

    return render_template(
        "index.html",
        movie=movie
    )

if __name__ == "__main__":
    app.run()
    