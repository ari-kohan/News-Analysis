from flask import Flask, render_template, request, jsonify, abort, g
from datetime import datetime, timedelta
import os
from guardian_api import GuardianAPI  # Assuming previous code is in guardian_api.py
import json
import sqlite3

from db import DATABASE, search_news, get_news_by_uid, get_all_news, insert_news
from rss_reader import read_rss_feeds


app = Flask(__name__)


def get_db():
    """Connect to the database"""
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


def init_db():
    """Initialize the database"""
    with app.app_context():
        db = get_db()
        with app.open_resource("schema.sql", mode="r") as f:
            db.cursor().executescript(f.read())
        db.commit()


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()


def setup():
    """Behavior before first request is executed"""
    # Initialize the database
    init_db()
    # Read RSS feeds
    news_data = read_rss_feeds()
    # Insert news into the database
    insert_news(get_db(), news_data)


with app.app_context():
    setup()


@app.route("/")
def index():
    try:
        # Get latest news
        results = get_all_news(get_db())

        return render_template(
            "index.html",
            articles=results,
            total_results=len(results),
        )
    except Exception as e:
        app.logger.error(f"Error fetching articles: {str(e)}")
        return render_template("index.html", error=str(e))


@app.route("/article/<path:uid>")
def article_detail(uid):
    try:
        article = get_news_by_uid(get_db(), uid)
        return render_template("article.html", article=article)
    except Exception as e:
        app.logger.error(f"Error fetching article {uid}: {str(e)}")
        abort(404)


@app.route("/search")
def search():
    query = request.args.get("q", "")

    if not query:
        return render_template("search.html")

    try:
        results = search_news(get_db(), query)
        return render_template(
            "search.html",
            articles=results,
            query=query,
            total_results=len(results),
            total_pages=1,
            current_page=1,
        )
    except Exception as e:
        app.logger.error(f"Error searching articles: {str(e)}")
        return render_template("search.html", error=str(e))


# API endpoints for AJAX requests
# @app.route('/api/search')
# def api_search():
#     query = request.args.get('q', '')
#     page = int(request.args.get('page', 1))

#     try:
#         results = guardian.search_articles(query=query, page=page)
#         return jsonify(results)
#     except Exception as e:
#         return jsonify({'error': str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True)
