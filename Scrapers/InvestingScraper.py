import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import os

def scrape_business_insider():
    url = "https://www.businessinsider.com/"

    # Selenium Chrome options
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

    html = driver.page_source
    driver.quit()

    os.makedirs("Debug", exist_ok=True)
    with open("Debug/business_insider_debug.html", "w", encoding="utf-8") as f:
        f.write(html)

    soup = BeautifulSoup(html, "html.parser")
    articles = []

   
    headline_tags = soup.find_all(["h2", "h3"])
    print(f"Found {len(headline_tags)} headline tags")

    for tag in headline_tags:
        a_tag = tag.find("a")
        if not a_tag:
            continue

        link = a_tag.get("href")
        
        if not link or not link.startswith("/"):
            continue

        headline = a_tag.get_text(strip=True)
        full_link = "https://www.businessinsider.com" + link

        articles.append({
            "Headline": headline,
            "Link": full_link,
            "Summary": "No summary"  
        })

    df = pd.DataFrame(articles)
    os.makedirs("Articles", exist_ok=True)
    df.to_csv("Articles/business_insider_articles.csv", index=False, encoding="utf-8")
    print("Saved Articles/business_insider_articles.csv")

if __name__ == "__main__":
    scrape_business_insider()
