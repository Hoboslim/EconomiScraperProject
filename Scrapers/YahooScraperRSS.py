import feedparser
import pandas as pd
import os

url = "https://finance.yahoo.com/rss/topstories"
feed = feedparser.parse(url)

articles = []
for entry in feed.entries[:50]:
    articles.append({
        "Headline": entry.title,
        "Link": entry.link,
        "Summary": getattr(entry, "summary", "No summary")
    })

df = pd.DataFrame(articles)
os.makedirs("Articles", exist_ok=True)
df.to_csv("Articles/yahoo_articles.csv", index=False, encoding="utf-8")
print("Saved Articles/yahoo_articles.csv")
