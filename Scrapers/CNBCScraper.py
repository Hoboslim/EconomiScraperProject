import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import os

def get_article_summary(url, driver):
    """Get the first few paragraphs of the article as a summary."""
    try:
        driver.get(url)
        time.sleep(2)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        paragraphs = soup.find_all("p")
        summary = " ".join(p.get_text(strip=True) for p in paragraphs[:3])
        return summary if summary else "No summary"
    except Exception as e:
        print(f"Error fetching summary for {url}: {e}")
        return "No summary"

def scrape_cnbc(max_articles=20):
    """
    Scrape CNBC business articles.

    Parameters:
    max_articles (int): Maximum number of articles to scrape. Default is 20.
    """
    url = "https://www.cnbc.com/business/"
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

    soup = BeautifulSoup(driver.page_source, "html.parser")
    articles = []

    headline_tags = soup.find_all("a", class_=["Card-title", "FeaturedCard-packagedCardTitle"])
    print(f"Found {len(headline_tags)} headline links")

    count = 0
    for tag in headline_tags:
        if count >= max_articles:
            break

        headline = tag.get_text(strip=True)
        link = tag.get("href")
        if not link:
            continue
        if not link.startswith("http"):
            link = "https://www.cnbc.com" + link

        summary = get_article_summary(link, driver)

        articles.append({
            "Headline": headline,
            "Link": link,
            "Summary": summary
        })

        count += 1

    driver.quit()

    df_new = pd.DataFrame(articles)
    os.makedirs("Articles", exist_ok=True)
    csv_path = "Articles/cnbc_articles.csv"

    
    if os.path.exists(csv_path):
        df_existing = pd.read_csv(csv_path)
        df_combined = pd.concat([df_existing, df_new], ignore_index=True)
        df_combined = df_combined.drop_duplicates(subset="Link", keep="first")
    else:
        df_combined = df_new

    df_combined.to_csv(csv_path, index=False, encoding="utf-8")
    print(f"Saved {csv_path} with {len(df_combined)} total articles")

if __name__ == "__main__":
    scrape_cnbc(max_articles=20)  
