import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import os
import time
from datetime import datetime

def scrape_investing(max_articles=50, stop_flag=lambda: False):
    url = "https://www.investing.com/news/"
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1920,1080")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
    )

    driver = webdriver.Chrome(options=options)
    driver.get(url)
    time.sleep(5)  

    soup = BeautifulSoup(driver.page_source, "html.parser")
    articles = []

    article_tags = soup.find_all("article", attrs={"data-test": "article-item"})
    count = 0

    for article in article_tags:
        if stop_flag():  
            print("Stopping scraper as requested")
            break
        if count >= max_articles:
            break

        a_tag = article.find("a", attrs={"data-test": "article-title-link"})
        if not a_tag:
            continue
        headline = a_tag.get_text(strip=True)
        link = a_tag.get("href")
        if link and not link.startswith("http"):
            link = "https://www.investing.com" + link

        summary_tag = article.find("div", class_="mb-1 mt-2.5 flex")
        summary = summary_tag.get_text(strip=True) if summary_tag else "No summary"

        time_tag = article.find("time", attrs={"data-test": "article-publish-date"})
        if time_tag and time_tag.has_attr("datetime"):
            date = time_tag["datetime"].split(" ")[0]
        else:
            date = datetime.now().strftime("%Y-%m-%d")

        articles.append({
            "Headline": headline,
            "Link": link,
            "Summary": summary,
            "Date": date,
            "Classified": False
        })

        count += 1

    driver.quit()

    df_new = pd.DataFrame(articles)
    os.makedirs("Articles", exist_ok=True)
    csv_path = "Articles/investing_articles.csv"

    if os.path.exists(csv_path):
        df_existing = pd.read_csv(csv_path)
        if "Classified" not in df_existing.columns:
            df_existing["Classified"] = True
        df_combined = pd.concat([df_existing, df_new], ignore_index=True)
        df_combined = df_combined.drop_duplicates(subset="Link", keep="first")
    else:
        df_combined = df_new

    df_combined.to_csv(csv_path, index=False, encoding="utf-8")
    print(f"Saved {csv_path} with {len(df_combined)} total articles")


def run_scraper(stop_flag=lambda: False):
    scrape_investing(max_articles=50, stop_flag=stop_flag)

if __name__ == "__main__":
    run_scraper()
