from flask import Flask, render_template, request, jsonify, abort
from datetime import datetime, timedelta
import os
from guardian_api import GuardianAPI  # Assuming previous code is in guardian_api.py
import json

from db import search_news, get_news_by_uid, get_all_news

app = Flask(__name__)

# Configure Guardian API
# GUARDIAN_API_KEY = os.getenv('GUARDIAN_API_KEY')
# guardian = GuardianAPI(GUARDIAN_API_KEY)

# Create templates folder with following files:
"""
templates/
    base.html
    index.html
    article.html
    search.html
"""


@app.route("/")
def index():
    try:
        # Get latest news
        results = get_all_news()

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
        article = get_news_by_uid(uid)
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
        results = search_news(query)
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
