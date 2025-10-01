import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import os
import time

def scrape_dn():
    url = "https://www.dn.se/ekonomi/"
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
    with open ("Debug/dn_debug.html", "w", encoding="utf-8") as f:
        f.write(html)

    soup = BeautifulSoup(html, "html.parser")
    articles =[]

    headline_tags = soup.find_all("a", class_="ds-teaser")
    print(f"Found {len(headline_tags)} headline links")

    for tag in headline_tags[:20]:
        link = tag.get("href")
        if link and not link.startswith("/"):
            link = "https://www.dn.se/ekonomi/" + link

        headline_tag = tag.find("h2", class_="ds-teaser__title")
        headline = headline_tag.get_text(strip=True) if headline_tag else "No headline"

        summary_tag = tag.find("p", class_="ds-teaser__text")
        summary = summary_tag.get_text(strip=True) if summary_tag else "No summary"

       
        articles.append({
            "Headline": headline,
            "Link": link,
            "Summary": summary
        })

    driver.quit()
    df = pd.DataFrame(articles)
    os.makedirs("Articles", exist_ok=True)
    df.to_csv("Articles/dn_articles.csv", index=False, encoding="utf-8")
    print("Saved Articles/dn_articles.csv")

if __name__ == "__main__":
    scrape_dn()