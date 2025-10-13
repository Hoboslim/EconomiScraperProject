import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import os
from datetime import datetime

def scrape_aftonbladet(max_articles=50):
    url = "https://www.aftonbladet.se/minekonomi/"
    
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
    driver.quit()

    os.makedirs("Debug", exist_ok=True)
    with open("Debug/aftonbladet_debug.html", "w", encoding="utf-8") as f:
        f.write(html)

    soup = BeautifulSoup(html, "html.parser")
    articles = []

    headline_tags = soup.find_all("div", class_="hyperion-css-1ooqwy6")
    print(f"Found {len(headline_tags)} article blocks")

    count = 0
    scrape_date = datetime.now().strftime("%Y-%m-%d")

    for tag in headline_tags:
        if count >= max_articles:
            break

        link_tag = tag.find("a", attrs={"data-test-tag": "internal-link"})
        link = link_tag.get("href") if link_tag else None
        if not link:
            continue

        if not link.startswith("/minekonomi/"):
            link = "/minekonomi/" + link
        full_link = "https://www.aftonbladet.se" + link

        headline_tag = tag.find("h2")
        headline = headline_tag.get_text(strip=True) if headline_tag else "No headline"

        summary_tag = tag.find("p")
        summary = summary_tag.get_text(strip=True) if summary_tag else "No summary"

        if "abplus" in summary.lower():
            continue

        articles.append({
            "Headline": headline,
            "Link": full_link,
            "Summary": summary,
            "Scraped_Date": scrape_date,
            "Classified": False  
        })

        count += 1

    df_new = pd.DataFrame(articles)
    os.makedirs("Articles", exist_ok=True)
    csv_path = "Articles/aftonbladet_articles.csv"

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
    scrape_aftonbladet(max_articles=50)
