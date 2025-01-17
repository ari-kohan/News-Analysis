from typing import List
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import json
from logging import log

from data_ingestors.rss_reader import RSSReader


def delete_collection(coll_ref, batch_size: int = 10):
    if batch_size == 0:
        return

    docs = coll_ref.list_documents(page_size=batch_size)
    deleted = 0

    for doc in docs:
        print(f"Deleting doc {doc.id} => {doc.get().to_dict()}")
        doc.delete()
        deleted = deleted + 1

    if deleted >= batch_size:
        return delete_collection(coll_ref, batch_size)


def add_rss_readers_to_firebase(db):
    for source in RSSReader.__subclasses__():
        s = source()
        reader = {
            "name": type(s).__name__,
            "type": s.type.name,
            "url": s.url,
            "last_etag": None,
            "last_fetched": None,
        }

        db.collection("Data Sources").document(reader["name"]).set(reader)


def update_rss_etag_and_timestamp(db, name, etag):
    db.collection("Data Sources").document(name).update(
        {"last_etag": etag, "last_fetched": firestore.SERVER_TIMESTAMP}
    )


def fetch_and_store_source_data(db):
    """
    Retrieve all data from the rss/api (only rss rn) sources, if it is new data
    (determined by a unique uid hashed from the url) add it to the firestore db
    """
    article_ids = db.collection("article_ids").document("id").get().to_dict()
    existing_articles = []
    if article_ids:
        existing_articles = set(article_ids["articles"])
    new_articles = []
    for reader in RSSReader.__subclasses__():
        r = reader()
        name = type(r).__name__
        reader_data = db.collection("Data Sources").document(name).get()
        reader_data = reader_data.to_dict()
        if not reader_data:
            log.warning(f"Could not find firestore data for reader {name}")
            return
        last_fetched = reader_data["last_fetched"]
        last_etag = reader_data["last_etag"]
        data, new_etag = r.fetch(last_fetched, last_etag)
        data = r.clean_data(data)
        data = r.format_data(data)
        update_rss_etag_and_timestamp(db, name, new_etag)
        for d in data:
            if d["uid"] not in existing_articles:
                d["analysed"] = True
                db.collection("articles").document(d["uid"]).set(d)
                new_articles.append(d["uid"])
    if new_articles:
        db.collection("article_ids").document("id").update(
            {"articles": firestore.ArrayUnion(new_articles)}
        )
    return new_articles


if __name__ == "__main__":
    # Fetch the service account key JSON file contents
    cred = credentials.Certificate("news_retriever.local.json")

    # Initialize the app with a service account, granting admin privileges
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    print(db._client_info.__dict__)
    # add_rss_readers_to_firebase(db)
    # fetch_source_data(db)

    # Store existing articles for ease of lookup
    # articles = []
    # for a in db.collection('articles').stream():
    #     articles.append(a.id)
    # print(articles)
    # db.collection("article_ids").document("id").set({"articles": articles})
    print(db.collection("article_ids").document("id").get().to_dict())
