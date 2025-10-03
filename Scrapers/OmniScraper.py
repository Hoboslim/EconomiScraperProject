import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import os
import time

def scrape_omni():
    url = "https://omni.se/ekonomi"

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
    for _ in range(3):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE_TIME)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    html = driver.page_source
    driver.quit()

    os.makedirs("Debug", exist_ok=True)
    with open("Debug/omni_debug.html", "w", encoding="utf-8") as f:
        f.write(html)

    soup = BeautifulSoup(html, "html.parser")
    articles = []

   
    teaser_links = soup.find_all("a", href=True)
    print(f"Found {len(teaser_links)} <a> tags")

    for a_tag in teaser_links:
       
        teaser_div = a_tag.find("div", class_="Teaser_teaserContent__e8paS")
        if not teaser_div:
            continue

        
        h2_tag = teaser_div.find("h2")
        if not h2_tag:
            continue
        headline = h2_tag.get_text(strip=True)

       
        p_tag = teaser_div.find("p")
        summary = p_tag.get_text(strip=True) if p_tag else "No summary"

       
        link = a_tag.get("href")
        if not link.startswith("http"):
            link = "https://omni.se" + link

        articles.append({
            "Headline": headline,
            "Link": link,
            "Summary": summary
        })

    
    df_new = pd.DataFrame(articles)
    os.makedirs("Articles", exist_ok=True)
    csv_path = "Articles/omni_articles.csv"

    if os.path.exists(csv_path):
        df_existing = pd.read_csv(csv_path)
        df_combined = pd.concat([df_existing, df_new], ignore_index=True)
        df_combined = df_combined.drop_duplicates(subset="Link", keep="first")
    else:
        df_combined = df_new

    df_combined.to_csv(csv_path, index=False, encoding="utf-8")
    print(f"Saved {csv_path} with {len(df_combined)} total articles")

if __name__ == "__main__":
    scrape_omni()
