import requests
from datetime import datetime, timedelta
import time


class GuardianAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://content.guardianapis.com"

    def get_article(self, article_id):
        """
        Fetch a single article by ID
        Example ID format: technology/2024/mar/15/article-slug-here
        """
        url = f"{self.base_url}/{article_id}"
        params = {
            "api-key": self.api_key,
            "show-fields": "all",  # Get all available fields including body text
        }

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()

            data = response.json()
            if data["response"]["status"] == "ok":
                content = data["response"]["content"]

                # Extract relevant fields
                article = {
                    "id": content["id"],
                    "type": content["type"],
                    "section_name": content["sectionName"],
                    "title": content["webTitle"],
                    "web_url": content["webUrl"],
                    "api_url": content["apiUrl"],
                    "publication_date": content["webPublicationDate"],
                }

                # Add fields if they exist
                if "fields" in content:
                    fields = content["fields"]
                    article.update(
                        {
                            "body_text": fields.get("bodyText"),
                            "body_html": fields.get("body"),
                            "headline": fields.get("headline"),
                            "thumbnail": fields.get("thumbnail"),
                            "word_count": fields.get("wordcount"),
                            "author": fields.get("byline"),
                        }
                    )

                return article
            else:
                raise Exception(f"API returned status: {data['response']['status']}")

        except requests.exceptions.RequestException as e:
            raise Exception(f"Error fetching article: {str(e)}")

    def search_articles(self, query, from_date=None, page=1, page_size=10):
        """
        Search for articles using various parameters
        """
        url = f"{self.base_url}/search"

        # If no from_date specified, default to last 30 days
        if from_date is None:
            from_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")

        params = {
            "api-key": self.api_key,
            "q": query,
            "from-date": from_date,
            "page": page,
            "page-size": page_size,
            "show-fields": "all",
            "order-by": "newest",
        }

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()

            data = response.json()
            if data["response"]["status"] == "ok":
                results = []
                for result in data["response"]["results"]:
                    article = {
                        "id": result["id"],
                        "type": result["type"],
                        "title": result["webTitle"],
                        "section_name": result["sectionName"],
                        "web_url": result["webUrl"],
                        "api_url": result["apiUrl"],
                        "publication_date": result["webPublicationDate"],
                    }

                    if "fields" in result:
                        fields = result["fields"]
                        article.update(
                            {
                                "body_text": fields.get("bodyText"),
                                "body_html": fields.get("body"),
                                "headline": fields.get("headline"),
                                "thumbnail": fields.get("thumbnail"),
                                "word_count": fields.get("wordcount"),
                                "author": fields.get("byline"),
                            }
                        )

                    results.append(article)

                return {
                    "articles": results,
                    "current_page": data["response"]["currentPage"],
                    "pages": data["response"]["pages"],
                    "total_results": data["response"]["total"],
                }
            else:
                raise Exception(f"API returned status: {data['response']['status']}")

        except requests.exceptions.RequestException as e:
            raise Exception(f"Error searching articles: {str(e)}")


# Example usage
if __name__ == "__main__":
    API_KEY = "your-api-key-here"
    guardian = GuardianAPI(API_KEY)

    # Example 1: Search for articles about AI
    results = guardian.search_articles(
        query="artificial intelligence", from_date="2024-01-01", page_size=5
    )

    print(f"Found {results['total_results']} articles")
    for article in results["articles"]:
        print(f"\nTitle: {article['title']}")
        print(f"Date: {article['publication_date']}")
        print(f"URL: {article['web_url']}")
        if article.get("body_text"):
            print(f"Preview: {article['body_text'][:200]}...")

    # Example 2: Fetch a specific article
    article_id = (
        "technology/2024/mar/15/example-article"  # Replace with real article ID
    )
    try:
        article = guardian.get_article(article_id)
        print(f"\nFull article: {article['title']}")
        print(f"Author: {article.get('author', 'Unknown')}")
        print(f"Word count: {article.get('word_count', 'Unknown')}")
    except Exception as e:
        print(f"Error: {str(e)}")
