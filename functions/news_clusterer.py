from datetime import datetime
from typing import List, Optional, Tuple
from data_ingestors.data import NewsData, EventCluster, NewsAnalysis
import hashlib
import logging
import sys
from sqlalchemy.exc import SQLAlchemyError

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class NewsClusterer:
    def __init__(self, time_window_hours: int = 24):
        self.time_window_hours = time_window_hours
        
    def calculate_temporal_similarity(self, date1: datetime, date2: datetime) -> float:
        """Calculate temporal similarity based on time difference."""
        time_diff_hours = abs((date1 - date2).total_seconds()) / 3600
        if time_diff_hours > self.time_window_hours:
            return 0.0
        return 1.0 - (time_diff_hours / self.time_window_hours)

    def calculate_location_similarity(self, places1: List[str], places2: List[str]) -> float:
        """Calculate Jaccard similarity between location sets."""
        if not places1 or not places2:
            return 0.0
        set1 = set(places1)
        set2 = set(places2)
        intersection = len(set1.intersection(set2))
        union = len(set1.union(set2))
        return intersection / union if union > 0 else 0.0

    def calculate_entity_similarity(self, article1: NewsData, article2: NewsData) -> float:
        """Calculate weighted similarity between other entities."""
        weights = {
            "people": 0.6,
            "agencies": 0.4
        }
        similarities = []
        
        # Compare people
        people1 = set(article1.analysis.people)
        people2 = set(article2.analysis.people)
        if people1 and people2:
            intersection = len(people1.intersection(people2))
            union = len(people1.union(people2))
            similarities.append((intersection / union if union > 0 else 0.0) * weights["people"])
        else:
            similarities.append(0.0)
            
        # Compare agencies
        agencies1 = set(article1.analysis.agencies)
        agencies2 = set(article2.analysis.agencies)
        if agencies1 and agencies2:
            intersection = len(agencies1.intersection(agencies2))
            union = len(agencies1.union(agencies2))
            similarities.append((intersection / union if union > 0 else 0.0) * weights["agencies"])
        else:
            similarities.append(0.0)
            
        return sum(similarities) / sum(weights.values())

    def calculate_similarity_score(
        self,
        article1: NewsData,
        article2: NewsData
    ) -> float:
        """Calculate overall similarity score between two articles."""
        # Calculate temporal similarity (highest weight: 0.4)
        temporal_sim = self.calculate_temporal_similarity(
            article1.date,
            article2.date
        )
        
        # If articles are too far apart in time, return 0
        if temporal_sim == 0:
            return 0.0
        
        # Calculate location similarity (weight: 0.35)
        location_sim = self.calculate_location_similarity(
            article1.analysis.places,
            article2.analysis.places
        )
        
        # Calculate other entity similarity (weight: 0.25)
        entity_sim = self.calculate_entity_similarity(article1, article2)
        
        # Calculate weighted sum
        weights = {
            'temporal': 0.4,
            'location': 0.35,
            'entity': 0.25
        }
        
        final_score = (
            weights['temporal'] * temporal_sim +
            weights['location'] * location_sim +
            weights['entity'] * entity_sim
        )
        
        return final_score

    def find_best_matching_cluster(
        self,
        article: NewsData,
        existing_clusters: List[EventCluster],
        similarity_threshold: float = 0.7
    ) -> Tuple[Optional[EventCluster], float]:
        """Find the best matching cluster for a new article."""
        best_cluster = None
        best_score = 0.0

        for cluster in existing_clusters:
            # Only consider clusters within the time window
            if abs((article.date - cluster.end_date).total_seconds()) > (self.time_window_hours * 3600):
                continue

            # Calculate similarity with cluster properties
            temporal_sim = self.calculate_temporal_similarity(article.date, cluster.end_date)
            location_sim = self.calculate_location_similarity(article.analysis.places, cluster.locations)
            
            # Calculate entity similarity using key entities
            entity_sim = self.calculate_location_similarity(
                article.analysis.people + article.analysis.agencies,
                cluster.key_entities
            )

            # Calculate weighted score
            score = (
                0.4 * temporal_sim +
                0.35 * location_sim +
                0.25 * entity_sim
            )

            if score > best_score and score >= similarity_threshold:
                best_score = score
                best_cluster = cluster

        return best_cluster, best_score

    def create_new_cluster(self, article: NewsData) -> EventCluster:
        """Create a new event cluster from an article."""
        cluster_id = hashlib.sha256(
            f"{article.uid}_{article.date.isoformat()}".encode()
        ).hexdigest()[:16]

        return EventCluster(
            uid=cluster_id,
            title=article.title,
            start_date=article.date,
            end_date=article.date,
            article_ids=[article.uid],
            primary_location=article.analysis.places[0] if article.analysis.places else "",
            locations=article.analysis.places,
            key_entities=article.analysis.people + article.analysis.agencies,
            tags=article.analysis.tags
        )

    def update_cluster(self, cluster: EventCluster, article: NewsData) -> EventCluster:
        """Update cluster with information from new article."""
        cluster.article_ids.append(article.uid)
        cluster.end_date = max(cluster.end_date, article.date)
        
        # Update locations
        new_locations = set(cluster.locations)
        new_locations.update(article.analysis.places)
        cluster.locations = list(new_locations)

        # Update key entities
        new_entities = set(cluster.key_entities)
        new_entities.update(article.analysis.people)
        new_entities.update(article.analysis.agencies)
        cluster.key_entities = list(new_entities)

        # Update tags
        new_tags = set(cluster.tags)
        new_tags.update(article.analysis.tags)
        cluster.tags = list(new_tags)

        return cluster

    def process_new_articles(
        self,
        new_articles: List[NewsData],
        existing_clusters: List[EventCluster],
        similarity_threshold: float = 0.7
    ) -> List[EventCluster]:
        """
        Process new articles and either add them to existing clusters or create new ones.
        
        Args:
            new_articles: List of new NewsData objects to process
            existing_clusters: List of existing EventCluster objects
            similarity_threshold: Minimum similarity score to consider articles related
            
        Returns:
            Updated list of all clusters
        """
        clusters = existing_clusters.copy()
        
        for article in new_articles:
            best_cluster, best_score = self.find_best_matching_cluster(
                article,
                clusters,
                similarity_threshold
            )
            
            if best_cluster:
                # Update existing cluster
                cluster_idx = clusters.index(best_cluster)
                clusters[cluster_idx] = self.update_cluster(best_cluster, article)
            else:
                # Create new cluster
                new_cluster = self.create_new_cluster(article)
                clusters.append(new_cluster)
        
        return clusters

if __name__ == "__main__":
    try:
        # Get all articles from db
        from db import get_engine, get_all_articles, insert_event_clusters, get_all_event_clusters
        
        try:
            engine = get_engine()
        except Exception as e:
            logger.error(f"Failed to create database engine: {str(e)}")
            sys.exit(1)
        
        try:
            articles = get_all_articles(engine)
            logger.info(f"Retrieved {len(articles)} articles from database")
        except SQLAlchemyError as e:
            logger.error(f"Failed to retrieve articles from database: {str(e)}")
            sys.exit(1)
        
        # Convert article dicts to NewsData objects
        news_data_list = []
        for article in articles:
            try:
                analysis = article['analysis']
                news_data = NewsData(
                    uid=str(article['id']),
                    title=article['title'],
                    content="",  # Content not needed for clustering
                    date=article['date'],
                    authors=article['authors'],
                    source=article['source'],
                    link=article['link'],
                    analysis=NewsAnalysis(
                        uid=str(article['id']),
                        summary=analysis['summary'],
                        people=analysis['people'] or [],  # Handle None values
                        places=analysis['places'] or [],
                        agencies=analysis['agencies'] or [],
                        laws=analysis['laws'] or [],
                        climate=analysis['climate'] or [],
                        tags=analysis['tags'] or []
                    )
                )
                news_data_list.append(news_data)
            except KeyError as e:
                logger.warning(f"Skipping article {article.get('id', 'unknown')}: Missing field {str(e)}")
            except Exception as e:
                logger.warning(f"Skipping article {article.get('id', 'unknown')}: {str(e)}")
        
        logger.info(f"Converted {len(news_data_list)} articles to NewsData objects")

        # Cluster them
        clusterer = NewsClusterer(time_window_hours=24)
        try:
            existing_clusters = get_all_event_clusters(engine)
            logger.info(f"Retrieved {len(existing_clusters)} existing clusters")
        except SQLAlchemyError as e:
            logger.error(f"Failed to retrieve existing clusters: {str(e)}")
            existing_clusters = []
            logger.info("Proceeding with empty cluster list")

        updated_clusters = clusterer.process_new_articles(news_data_list, existing_clusters)
        logger.info(f"Created/updated {len(updated_clusters)} clusters")

        # Add clusters to the db
        try:
            insert_event_clusters(engine, updated_clusters)
            logger.info("Successfully saved clusters to database")
        except SQLAlchemyError as e:
            logger.error(f"Failed to save clusters to database: {str(e)}")
            sys.exit(1)

        # Get all clusters from the db and display summary
        try:
            all_clusters = get_all_event_clusters(engine)
            print(f"\nTotal clusters: {len(all_clusters)}")
            for cluster in all_clusters:
                print(f"\nCluster: {cluster.title}")
                print(f"Date range: {cluster.start_date} to {cluster.end_date}")
                print(f"Articles: {len(cluster.article_ids)}")
                print(f"Locations: {', '.join(cluster.locations)}")
        except SQLAlchemyError as e:
            logger.error(f"Failed to retrieve final cluster list: {str(e)}")
            sys.exit(1)

    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        sys.exit(1)