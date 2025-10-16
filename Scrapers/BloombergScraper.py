import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from datetime import datetime
import os
import time

def run_scraper(max_articles=60, stop_flag=lambda: False):
    url = "https://www.bloomberg.com/"

    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(options=options)
    driver.get(url)

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a.StoryBlock_storyLink__5nXw8"))
        )
    except Exception as e:
        print(f"Error waiting for page elements: {e}")
        driver.quit()
        return

    if stop_flag():
        print("Scraper stopped before parsing.")
        driver.quit()
        return

    html = driver.page_source

    os.makedirs("Debug", exist_ok=True)
    with open("Debug/bloomberg_debug.html", "w", encoding="utf-8") as f:
        f.write(html)

    soup = BeautifulSoup(html, "html.parser")
    articles = []
    scrape_date = datetime.now().strftime("%Y-%m-%d")

    story_blocks = soup.find_all("a", class_="StoryBlock_storyLink__5nXw8")
    print(f"Found {len(story_blocks)} story blocks")

    count = 0

    for block in story_blocks:
        if stop_flag():
            print("Scraper stopped during article processing.")
            break

        if count >= max_articles:
            break

        headline_tag = block.find("div", attrs={"data-component": "headline"})
        headline = headline_tag.get_text(strip=True) if headline_tag else "No headline"

        link = block.get("href")
        if link and not link.startswith("http"):
            link = "https://www.bloomberg.com" + link

        summary_tag = (
            block.find("section", attrs={"data-component": "summary"}) or
            block.find("div", attrs={"data-component": "summary"}) or
            block.find("p")
        )
        summary = summary_tag.get_text(strip=True) if summary_tag else "No summary"

        articles.append({
            "Headline": headline,
            "Link": link,
            "Summary": summary,
            "Scraped_Date": scrape_date,
            "Classified": False
        })

        count += 1

    driver.quit()

    df_new = pd.DataFrame(articles)
    os.makedirs("Articles", exist_ok=True)
    csv_path = "Articles/bloomberg_articles.csv"

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
    run_scraper()
