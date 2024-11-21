from celery import Celery
from celery.schedules import crontab
import inspect

from rss_reader import RSSReader

# Initialize Celery
celery_app = Celery(
    "news_tracker",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0",
)

# Celery Configuration
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)

# Configure the periodic tasks
celery_app.conf.beat_schedule = {
    "fetch-rss-feeds": {
        "task": "celery_app.fetch_all_rss_feeds",
        "schedule": 30,  # 1.5 hours in seconds
        "options": {"expires": 60},
        "relative": True,
    },
}


@celery_app.task
def fetch_all_rss_feeds():
    """
    Find all RSSReader subclasses and execute their fetch, clean, and format methods
    """

    # Get all subclasses of RSSReader
    def get_all_subclasses(cls):
        all_subclasses = []
        for subclass in cls.__subclasses__():
            all_subclasses.append(subclass)
            all_subclasses.extend(get_all_subclasses(subclass))
        return all_subclasses

    rss_readers = get_all_subclasses(RSSReader)

    for reader_class in rss_readers:
        try:
            # Initialize the reader
            reader = reader_class()

            # Execute the pipeline
            data = reader.fetch()
            if data:  # Only process if we got new data
                cleaned_data = reader.clean_data(data)
                formatted_data = reader.format_data(cleaned_data)
                reader.save_data(formatted_data)
        except Exception as e:
            print(f"Error processing {reader_class.__name__}: {str(e)}")


if __name__ == "__main__":
    celery_app.start()
