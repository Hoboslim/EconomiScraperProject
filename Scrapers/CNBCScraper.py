import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import os

def get_article_summary_and_date(url, driver, stop_flag=lambda: False):
    try:
        if stop_flag():
            print(f"Scraper stopped before fetching summary for {url}")
            return "Scraper stopped", time.strftime("%Y-%m-%d")

        driver.get(url)
        time.sleep(2)
        if stop_flag():
            print(f"Scraper stopped during fetching summary for {url}")
            return "Scraper stopped", time.strftime("%Y-%m-%d")

        soup = BeautifulSoup(driver.page_source, "html.parser")
        paragraphs = soup.find_all("p")
        summary = " ".join(p.get_text(strip=True) for p in paragraphs[:3])
        time_tag = soup.find("time")
        if time_tag and time_tag.has_attr("datetime"):
            date = time_tag["datetime"]
        else:
            date = time.strftime("%Y-%m-%d")
        return summary if summary else "No summary", date
    except Exception as e:
        print(f"Error fetching summary for {url}: {e}")
        return "No summary", time.strftime("%Y-%m-%d")

def run_scraper(max_articles=50, stop_flag=lambda: False):
    url = "https://www.cnbc.com/business/"
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

    if stop_flag():
        print("Scraper stopped before parsing main page.")
        driver.quit()
        return

    soup = BeautifulSoup(driver.page_source, "html.parser")
    articles = []

    headline_tags = soup.find_all("a", class_=["Card-title", "FeaturedCard-packagedCardTitle"])
    print(f"Found {len(headline_tags)} headline links")

    count = 0
    for tag in headline_tags:
        if stop_flag():
            print("Scraper stopped during article processing.")
            break

        if count >= max_articles:
            break

        headline = tag.get_text(strip=True)
        link = tag.get("href")
        if not link:
            continue
        if not link.startswith("http"):
            link = "https://www.cnbc.com" + link

        summary, date = get_article_summary_and_date(link, driver, stop_flag=stop_flag)

        articles.append({
            "Headline": headline,
            "Link": link,
            "Summary": summary,
            "Scraped_Date": date,
            "Classified": False
        })

        count += 1

    driver.quit()

    df_new = pd.DataFrame(articles)
    os.makedirs("Articles", exist_ok=True)
    csv_path = "Articles/cnbc_articles.csv"

    if os.path.exists(csv_path):
        df_existing = pd.read_csv(csv_path)
        if "Classified" not in df_existing.columns:
            df_existing["Classified"] = True
        df_combined = pd.concat([df_existing, df_new], ignore_index=True)
        df_combined = df_combined.drop_duplicates(subset="Link", keep="first")
    else:
        df_combined = df_new

    df_combined.to_csv(csv_path, index=False, encoding="utf-8")
    print(f"Saved {csv_path} with {len(df_combined)} total articles")


if __name__ == "__main__":
    run_scraper(max_articles=50)
