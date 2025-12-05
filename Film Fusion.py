import os
import requests
import json
from flask import Flask, request, render_template, redirect, url_for
import webbrowser
from Recomender import Recomend
from tmdb import tmdb_get , tmdb_search_movies, get_trending
import time


app = Flask(__name__)
app.debug = False


@app.route("/", methods=["GET"])
def index():
    trends=[]
    for t in get_trending():
        if t:
            if t['media_type']=='movie':
                trends.append(t)

    return render_template("index.html", query="",trending=trends[:5], results=None)
    
@app.route("/search", methods=["POST"])
def search_post():
    query = request.form.get("query")
    if not query:
        return redirect(url_for("index", error="Query is required"))
    results = tmdb_search_movies(query, page=1)
    if "error" in results:
        return render_template("error.html", message=results["error"])
    return render_template("results.html", results=results["results"][:8], query=query, current_page=1, total_pages=results["total_pages"])


@app.route("/search_by_name")
def movie_search():
    return render_template("testing.html")

@app.route("/movie/<int:movie_id>")
def movie_detail(movie_id):
    try:
        # Fetch main movie details (details + videos in one request)
        movie = tmdb_get(f"/movie/{movie_id}", params={"append_to_response": "videos,images"})

        title = movie.get("title")

        # --- Get AI-based recommendations ---
        recommended_titles = Recomend(title)  # list of strings

        # TMDB search for each recommended title safely
        recommended_movies = []
        for t in recommended_titles:
            try:
                search_results = tmdb_get("/search/movie", params={"query": t, "page": 1}).get("results", [])
                if search_results:
                    recommended_movies.append(search_results[0])
                time.sleep(0.5)  # small delay between requests
            except Exception as e:
                print(f"TMDB search failed for {t}: {e}")
                continue  # skip failed searches

        # --- Fetch cast ---
        credits = tmdb_get(f"/movie/{movie_id}/credits").get("cast", [])[:10]

        # --- Fetch similar movies ---
        #similar_movies = tmdb_get(f"/movie/{movie_id}/similar").get("results", [])[:8]

        # --- Extract trailer ---
        trailer = None
        for vid in movie.get("videos", {}).get("results", []):
            if vid["type"] == "Trailer" and vid["site"] == "YouTube":
                trailer = vid["key"]
                break

        return render_template(
            "movie_detail.html",
            movie=movie,
            cast=credits,
            trailer=trailer,
            recommended_movies=recommended_movies
        )

    except Exception as e:
        return render_template("error.html", message=f"Failed to load movie data: {e}")


def format_date(date_str):
    if date_str:
        return f"{date_str[:4]}-{date_str[5:7]}-{date_str[8:10]}"
    return ""

@app.context_processor
def inject_format_date():
    return dict(format_date=format_date)

def main():
    if __name__ == "__main__":
        webbrowser.open("http://127.0.0.1:5000")
        app.run(host="0.0.0.0", port=5000)

if __name__ == "__main__":
    main()
