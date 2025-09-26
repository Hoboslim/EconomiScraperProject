import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import os

def get_article_summary(url, driver):
    driver.get(url)
    time.sleep(2)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    paragraphs = soup.find_all("p")
    summary = " ".join(p.get_text(strip=True) for p in paragraphs[:3])
    return summary if summary else "No summary"

def scrape_cnbc():
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

    for tag in headline_tags[:20]: 
        headline = tag.get_text(strip=True)
        link = tag.get("href")
        if link and not link.startswith("http"):
            link = "https://www.cnbc.com" + link

     
        summary = get_article_summary(link, driver)

        articles.append({
            "Headline": headline,
            "Link": link,
            "Summary": summary
        })

    driver.quit()

  
    df = pd.DataFrame(articles)
    os.makedirs("Articles", exist_ok=True)
    df.to_csv("Articles/cnbc_articles.csv", index=False, encoding="utf-8")
    print("Saved Articles/cnbc_articles.csv")

if __name__ == "__main__":
    scrape_cnbc()
