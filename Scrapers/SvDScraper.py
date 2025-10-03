import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import os

def scrape_svd():
    url = "https://www.svd.se/naringsliv"

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
    with open("Debug/svd_debug.html", "w", encoding="utf-8") as f:
        f.write(html)

    soup = BeautifulSoup(html, "html.parser")
    articles = []

    story_blocks = soup.find_all("div", class_="TeaserBody-www__sc-1maddnp-0")
    print(f"Found {len(story_blocks)} story blocks")

    for block in story_blocks[:50]:
        headline_tag = block.find("h2")
        headline = headline_tag.get_text(strip=True) if headline_tag else "No headline"

        summary_tag = block.find("p")
        summary = summary_tag.get_text(strip=True) if summary_tag else "No summary"

       
        a_tag = block.find_parent("a")
        link = a_tag["href"] if a_tag and a_tag.has_attr("href") else None
        if link and not link.startswith("http"):
            link = "https://www.svd.se" + link

        articles.append({
            "Headline": headline,
            "Link": link if link else "No link",
            "Summary": summary
        })

    
    df_new = pd.DataFrame(articles)
    os.makedirs("Articles", exist_ok=True)
    csv_path = "Articles/svd_articles.csv"

    if os.path.exists(csv_path):
        df_existing = pd.read_csv(csv_path)
        df_combined = pd.concat([df_existing, df_new], ignore_index=True)
        df_combined = df_combined.drop_duplicates(subset="Link", keep="first")
    else:
        df_combined = df_new

    df_combined.to_csv(csv_path, index=False, encoding="utf-8")
    print(f"Saved {csv_path} with {len(df_combined)} total articles")

if __name__ == "__main__":
    scrape_svd()
