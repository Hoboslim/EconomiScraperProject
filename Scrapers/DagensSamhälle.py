import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import os
import time
from datetime import datetime

def scrape_ds(max_articles=50):
    url = "https://www.dagenssamhalle.se/offentlig-ekonomi/"
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
    os.makedirs("Debug", exist_ok=True)
    with open("Debug/dagenssamhalle_debug.html", "w", encoding="utf-8") as f:
        f.write(html)

    soup = BeautifulSoup(html, "html.parser")
    articles = []
    scrape_date = datetime.now().strftime("%Y-%m-%d")

    for h2 in soup.find_all("h2", class_="css-1r7q9wq e1j4h7q20"):
        if len(articles) >= max_articles:
            break

        headline = h2.get_text(strip=True)
        a_tag = h2.find_parent("a")
        link = a_tag["href"] if a_tag and a_tag.has_attr("href") else None
        if link and not link.startswith("http"):
            link = "https://www.dagenssamhalle.se" + link

        
        summary_div = h2.find_next("div", class_="css-ky9fcu ej9i57d2")
        summary_p = summary_div.find("p", class_="css-u3rr24 e2uxtwg0") if summary_div else None
        summary = summary_p.get_text(strip=True) if summary_p else "No summary"

        articles.append({
            "Headline": headline,
            "Link": link,
            "Summary": summary,
            "Scraped_Date": scrape_date
        })

    driver.quit()

    df_new = pd.DataFrame(articles)
    os.makedirs("Articles", exist_ok=True)
    csv_path = "Articles/dagenssamhalle_articles.csv"

    if os.path.exists(csv_path):
        df_existing = pd.read_csv(csv_path)
        df_combined = pd.concat([df_existing, df_new], ignore_index=True)
        df_combined.drop_duplicates(subset="Link", inplace=True)
    else:
        df_combined = df_new

    df_combined.to_csv(csv_path, index=False, encoding="utf-8")
    print(f"Saved {csv_path} with {len(df_combined)} total articles")

if __name__ == "__main__":
    scrape_ds(max_articles=50)
