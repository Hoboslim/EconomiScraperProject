import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import os
import time
from datetime import datetime

def scrape_svt(max_articles=50):
    url = "https://www.svt.se/nyheter/ekonomi/"
    
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
    )

    driver = webdriver.Chrome(options=options)
    driver.get(url)
    time.sleep(5)

    html = driver.page_source
    driver.quit()

    os.makedirs("Debug", exist_ok=True)
    with open("Debug/svt_debug.html", "w", encoding="utf-8") as f:
        f.write(html)

    soup = BeautifulSoup(html, "html.parser")
    articles = []

    headline_blocks = soup.find_all("div", class_="FeedTeaser__content___ADWwY")
    print(f"Found {len(headline_blocks)} article blocks")
    
    scraped_date = datetime.now().strftime("%Y-%m-%d")
    count = 0

    for block in headline_blocks:
        if count >= max_articles:
            break

        headline_tag = block.find("h1")
        headline = headline_tag.get_text(strip=True) if headline_tag else "No Headline"

        link_tag = block.find_parent("a")
        link = link_tag.get("href") if link_tag else None
        if link and link.startswith("/"):
            link = "https://www.svt.se" + link

        summary_tag = block.find("div", class_="FeedTeaser__textContent___RLNUu")
        summary = summary_tag.get_text(strip=True) if summary_tag else "No summary"

        articles.append({
            "Headline": headline,
            "Link": link,
            "Summary": summary,
            "Scraped_Date": scraped_date,
            "Classified": False
        })

        count += 1

    df_new = pd.DataFrame(articles)
    os.makedirs("Articles", exist_ok=True)
    csv_path = "Articles/svt_articles.csv"

    if os.path.exists(csv_path):
        df_existing = pd.read_csv(csv_path)
        if "Classified" not in df_existing.columns:
            df_existing["Classified"] = True
        df_combined = pd.concat([df_existing, df_new], ignore_index=True)
        df_combined.drop_duplicates(subset="Link", keep="first", inplace=True)
    else:
        df_combined = df_new

    df_combined.to_csv(csv_path, index=False, encoding="utf-8")
    print(f"Saved {csv_path} with {len(df_combined)} total articles")


if __name__ == "__main__":
    scrape_svt(max_articles=50)
