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

def scrape_business_insider():
    url = "https://www.businessinsider.com/"

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

   
    SCROLL_PAUSE_TIME = 2
    last_height = driver.execute_script("return document.body.scrollHeight")
    for _ in range(5): 
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE_TIME)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    html = driver.page_source

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

       
        summary = get_article_summary(full_link, driver)

        articles.append({
            "Headline": headline,
            "Link": full_link,
            "Summary": summary
        })

    driver.quit()

    df = pd.DataFrame(articles)
    os.makedirs("Articles", exist_ok=True)
    df.to_csv("Articles/business_insider_articles.csv", index=False, encoding="utf-8")
    print("Saved Articles/business_insider_articles.csv")

if __name__ == "__main__":
    scrape_business_insider()
