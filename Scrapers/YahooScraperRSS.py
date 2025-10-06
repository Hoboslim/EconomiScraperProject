import feedparser
import pandas as pd
import os
from datetime import datetime

def scrape_yahoo_rss(max_articles=50):
    url = "https://finance.yahoo.com/rss/topstories"
    feed = feedparser.parse(url)
    articles = []

    scraped_date = datetime.now().strftime("%Y-%m-%d")
    count = 0

    for entry in feed.entries:
        if count >= max_articles:
            break

        headline = getattr(entry, "title", "No headline")
        link = getattr(entry, "link", "No link")
        summary = getattr(entry, "summary", "No summary")

        articles.append({
            "Headline": headline,
            "Link": link,
            "Summary": summary,
            "Scraped_Date": scraped_date
        })

        count += 1

    os.makedirs("Articles", exist_ok=True)
    csv_path = "Articles/yahoo_articles.csv"
    df_new = pd.DataFrame(articles)

    if os.path.exists(csv_path):
        df_existing = pd.read_csv(csv_path)
        df_combined = pd.concat([df_existing, df_new], ignore_index=True)
        df_combined = df_combined.drop_duplicates(subset="Link", keep="first")
    else:
        df_combined = df_new

    df_combined.to_csv(csv_path, index=False, encoding="utf-8")
    print(f"Saved {len(df_combined)} total articles to {csv_path}")

if __name__ == "__main__":
    scrape_yahoo_rss(max_articles=50)
