import feedparser
import pandas as pd
import os 

def scrape_marketwatch_rss():

    rss_url = "https://www.marketwatch.com/rss/topstories"
    
    feed = feedparser.parse(rss_url)
    articles = []
    
    for entry in feed.entries:
        headline = entry.get("title", "No headline")
        link = entry.get("link", "No link")
        summary = entry.get("summary", headline)
        
        articles.append({
            "Headline": headline,
            "link": link,
            "Summary": summary
            
        })
        
        os.makedirs("Articles", exist_ok=True)
        df = pd.DataFrame(articles)
        df.to_csv("Articles/marketwatch_articles.csv", index=False, encoding="utf-8")
        print(f"Saved{len(articles)} articles to Articles/marketwatch_articles.csv")
        
if __name__ == "__main__":
    scrape_marketwatch_rss()