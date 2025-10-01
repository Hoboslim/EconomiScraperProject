import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import os

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

    headline_tags = soup.find_all("div", attrs={"data-testid": "card-text-wrapper"})
    print(f"Found {len(headline_tags)} headline tags")

    for tag in headline_tags[:30]:
        headline_tag = tag.find("h2", attrs={"data-testid": "card-headline"})
        headline = headline_tag.get_text(strip=True) if headline_tag else "No headline"

        summary_tag = tag.find("p", attrs={"data-testid": "card-description"})
        summary = summary_tag.get_text(strip=True) if summary_tag else "No summary"

        parent_a = tag.find_parent("a")
        link = parent_a.get("href") if parent_a else "No link"
        if link and not link.startswith("/"):
            link = "https://www.bbc.com/business" + link

        articles.append({
            "Headline": headline,
            "Link": link or "No link",
            "Summary": summary
        })

    driver.quit()

    df_new = pd.DataFrame(articles)
    os.makedirs("Articles", exist_ok=True)
    csv_path = "Articles/bbc_articles.csv"

    if os.path.exists(csv_path):
       
        df_existing = pd.read_csv(csv_path)
        
        df_combined = pd.concat([df_existing, df_new], ignore_index=True)
        
        df_combined = df_combined.drop_duplicates(subset="Link", keep="first")
    else:
        df_combined = df_new

    df_combined.to_csv(csv_path, index=False, encoding="utf-8")
    print(f"Saved {csv_path} with {len(df_combined)} total articles")

if __name__ == "__main__":
    scrape_bbc()
