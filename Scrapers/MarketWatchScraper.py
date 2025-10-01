import feedparser
import pandas as pd
import os

def scrape_marketwatch_rss(max_articles=50):
    rss_url = "https://www.marketwatch.com/rss/topstories"
    feed = feedparser.parse(rss_url)
    articles = []

    count = 0
    for entry in feed.entries:
        if count >= max_articles:
            break

        headline = entry.get("title", "No headline")
        link = entry.get("link", "No link")
        summary = entry.get("summary", headline)

        articles.append({
            "Headline": headline,
            "Link": link,
            "Summary": summary
        })

        count += 1

    os.makedirs("Articles", exist_ok=True)
    csv_path = "Articles/marketwatch_articles.csv"
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
    scrape_marketwatch_rss(max_articles=50)
