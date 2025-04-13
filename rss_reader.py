# rss_reader.py

import feedparser
from datetime import datetime

# RSS feed URLs grouped by category
RSS_FEEDS = {
    "Technology": [
        "https://techcrunch.com/feed/",
        "https://www.wired.com/feed/rss",
        "https://www.technologyreview.com/feed/"
    ],
    "Finance": [
        "https://www.bloomberg.com/feed/podcast/etf-report.xml",
        "https://www.ft.com/?format=rss",
        "https://www.forbes.com/real-time/feed2/"
    ],
    "Sports": [
        "https://www.espn.com/espn/rss/news",
        "http://feeds.bbci.co.uk/sport/rss.xml",
        "https://www.skysports.com/rss/12040"
    ],
    "Entertainment": [
        "https://variety.com/feed/",
        "https://www.rollingstone.com/music/music-news/feed/",
        "https://www.billboard.com/feed/"
    ],
    "Science": [
        "https://www.nasa.gov/rss/dyn/breaking_news.rss",
        "https://www.sciencedaily.com/rss/all.xml",
        "https://feeds.arstechnica.com/arstechnica/science"
    ],
    "General News": [
        "http://feeds.bbci.co.uk/news/world/rss.xml",
        "https://rss.nytimes.com/services/xml/rss/nyt/World.xml",
        "http://feeds.reuters.com/reuters/topNews"
    ]
}

def fetch_articles():
    all_articles = []

    for category, feeds in RSS_FEEDS.items():
        for url in feeds:
            parsed_feed = feedparser.parse(url)
            for entry in parsed_feed.entries:
                article = {
                    "title": entry.get("title", "No Title"),
                    "link": entry.get("link", ""),
                    "summary": entry.get("summary", "No Summary"),
                    "published": entry.get("published", ""),
                    "category": category,
                    "source": parsed_feed.feed.get("title", "Unknown Source")
                }
                all_articles.append(article)
    
    return all_articles

# Run test
if __name__ == "__main__":
    articles = fetch_articles()
    print(f"Fetched {len(articles)} articles.")
    print(articles[0] if articles else "No articles found.")
