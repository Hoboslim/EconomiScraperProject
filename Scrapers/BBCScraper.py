import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import os
import requests

def scrape_bbc():
    url = "https://www.bbc.com/business"
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
    os.makedirs("Debug", exist_ok=True)
    with open("Debug/bbc_debug.html", "w", encoding="utf-8") as f:
        f.write(html)

    soup = BeautifulSoup(html, "html.parser")
    articles = []

    headline_tags = soup.find_all("div",attrs={"datatest-id" : "card-text-wrapper"})
    print(f"Found {len(headline_tags)} headline links")

    for tag in headline_tags[:20]:

        headline_tag = tag.find("h2", attrs={"datatest-id" : "card-headline"})
        headline = headline_tag.get_text(strip=True) if headline_tag else "No headline"

        summary_tag = tag.find("p", attrs={"datatest-id": "card-description"})
        summary = summary_tag.get_text(strip=True) if summary_tag else "No summary"

        parent_a = tag.find_parent("a")
        link =parent_a.get("href") if parent_a else "No link"
        
        if link and not link.startswith("/"):
        link= "https://www.bbc.com/business" + link

        articles.append({
            "Headline": headline,
            "Link": link or "No link",
            "Summary": summary
        })

    driver.quit()
    df = pd.DataFrame(articles)
    os.makedirs("Articles", exist_ok=True)
    df.to_csv("Articles/bbc_articles.csv", index=False, encoding="utf-8")
    print("Saved Articles/bbc_articles.csv")

if __name__ == "__main__":
    scrape_bbc()
