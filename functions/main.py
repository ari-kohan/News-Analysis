# Welcome to Cloud Functions for Firebase for Python!
# To get started, simply uncomment the below code or create your own.
# Deploy with `firebase deploy`
from typing import Any

from firebase_functions import https_fn, scheduler_fn
from firebase_admin import initialize_app, firestore
from firestore_interface import fetch_and_store_source_data, add_rss_readers_to_firebase
from llm_interface import analyse_articles
from db import insert_news


initialize_app()


@https_fn.on_call()
def db_init_utils(_: https_fn.CallableRequest) -> Any:
    """Handle db setup when testing functionality"""
    db = firestore.client()
    add_rss_readers_to_firebase(db)
    db.collection("article_ids").document("id").set({"articles": []})


@scheduler_fn.on_schedule(schedule="every day 00:00")
def news_retriever(_: scheduler_fn.ScheduledEvent) -> None:
    """
    Retrieve the news from sources defined in data_ingestors and store it
    in the firestore db
    :param event: The event triggered at midnight
    """
    db = firestore.client()
    new_articles = fetch_and_store_source_data(db)
    news_data = analyse_articles(new_articles)
    insert_news(news_data)
