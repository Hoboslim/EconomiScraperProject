import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import os
import time

def scrape_expressen():
    url = "https://www.expressen.se/ekonomi/"
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
    with open("Debug/expressen_debug.html", "w", encoding="utf-8") as f:
        f.write(html)
    
    soup = BeautifulSoup(html, "html.parser")
    articles = []

    headline_tags = soup.find_all("div", class_="teaser")
    print(f"Found {len(headline_tags)} headline links")

    for tag in headline_tags[:20]:
        a_tag = tag.find("a")
        if not a_tag:
            continue

        link = a_tag.get("href") 
        if not link or not link.startswith("/ekonomi/"):
            link = "https://www.expressen.se/ekonomi/" + link


        headline_tag = tag.find("h2")
        headline = headline_tag.get_text(strip=True) if headline_tag else "No headline"

        summary_tag = tag.find("p")
        summary = summary_tag.get_text(strip= True) if summary_tag else "No headline"


        articles.append({
            "Headline": headline,
            "Link": link,
            "Summary": summary
        })

    driver.quit()
    df = pd.DataFrame(articles)
    os.makedirs("Articles", exist_ok=True)
    df.to_csv("Articles/expressen_articles.csv", index=False, encoding="utf-8")
    print("Saved Articles/expressen_articles.csv")

if __name__ == "__main__":
    scrape_expressen()
