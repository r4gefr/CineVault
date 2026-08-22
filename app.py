from flask import Flask, render_template, request, redirect, url_for
from dotenv import load_dotenv
import requests
import os

load_dotenv()

app = Flask(__name__)

api_key = os.getenv("OMDB_API_KEY")


def format_votes(votes):
    if not votes or votes == "N/A":
        return "N/A"

    try:
        votes = int(votes.replace(",", ""))
    except (ValueError, AttributeError):
        return "N/A"

    if votes >= 1_000_000:
        value = f"{votes / 1_000_000:.1f}".rstrip("0").rstrip(".")
        return f"{value}M"

    elif votes >= 1_000:
        value = f"{votes / 1_000:.1f}".rstrip("0").rstrip(".")
        return f"{value}K"

    return str(votes)


@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":

        movie_name = request.form.get("movie", "").strip()

        if movie_name:
            return redirect(
                url_for(
                    "movie_page",
                    movie_name=movie_name
                )
            )

    return render_template("index.html")


@app.route("/movie/<movie_name>")
def movie_page(movie_name):

    movie = None
    error = None

    url = f"https://www.omdbapi.com/?t={movie_name}&apikey={api_key}"

    try:

        response = requests.get(url, timeout=5)
        response.raise_for_status()

        data = response.json()

        if data["Response"] == "True":

            data["formatted_votes"] = format_votes(data["imdbVotes"])

            movie = data

        else:
            error = data.get("Error", "Movie not found.")

    except requests.RequestException:
        error = "Unable to connect to the movie database."

    return render_template(
        "movie.html",
        movie=movie,
        error=error
    )


if __name__ == "__main__":
    app.run(debug=True)