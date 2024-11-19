from flask import Flask, render_template, request, jsonify, abort
from datetime import datetime, timedelta
import os
from guardian_api import GuardianAPI  # Assuming previous code is in guardian_api.py
import json

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

@app.route('/')
def index():
    try:
        # Get latest news
        results = json.load(open('rss_feed_0.json'))
        
        return render_template(
            'index.html',
            articles=results,
            total_results=len(results),
        )
    except Exception as e:
        app.logger.error(f"Error fetching articles: {str(e)}")
        return render_template('index.html', error=str(e))

@app.route('/article/<path:uid>')
def article_detail(uid):
    results = json.load(open('rss_feed_0.json'))
    try:
        article = next((item for item in results if item['uid'] == uid))
        return render_template('article.html', article=article)
    except Exception as e:
        app.logger.error(f"Error fetching article {uid}: {str(e)}")
        abort(404)

# @app.route('/search')
# def search():
#     query = request.args.get('q', '')
#     page = int(request.args.get('page', 1))
    
#     if not query:
#         return render_template('search.html')
        
#     try:
#         results = guardian.search_articles(
#             query=query,
#             page=page,
#             page_size=20
#         )
#         return render_template(
#             'search.html',
#             articles=results['articles'],
#             query=query,
#             current_page=results['current_page'],
#             total_pages=results['pages'],
#             total_results=results['total_results']
#         )
#     except Exception as e:
#         app.logger.error(f"Error searching articles: {str(e)}")
#         return render_template('search.html', error=str(e))

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

if __name__ == '__main__':
    app.run(debug=True)