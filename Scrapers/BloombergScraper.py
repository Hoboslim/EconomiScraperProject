import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import os
import requests
from urllib.parse import urljoin

def get_article_summary(article_url):
    """Fetch the first paragraph from the article page as a fallback summary."""
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(article_url, headers=headers, timeout=10)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, "html.parser")
            body = soup.find("section", attrs={"data-component": "body"})
            if body:
                first_p = body.find("p")
                if first_p:
                    return first_p.get_text(strip=True)
    except Exception as e:
        print(f"Error fetching {article_url}: {e}")
    return "No summary"

def scrape_bloomberg():
    url = "https://www.bloomberg.com/"
    options = Options()
    
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(options=options)
    driver.get(url)

    
    story_blocks = []
    print("Waiting for story blocks to load...")
    while True:
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        story_blocks = soup.find_all("a", class_="StoryBlock_storyLink__5nXw8")
        if story_blocks:
            print(f"Found {len(story_blocks)} story blocks!")
            break
        print("Story blocks not loaded yet, waiting 1 second...")
        time.sleep(1)

   
    os.makedirs("Debug", exist_ok=True)
    with open("Debug/bloomberg_debug.html", "w", encoding="utf-8") as f:
        f.write(html)

    articles = []
    for i, block in enumerate(story_blocks[:50]):
      
        headline_tag = block.find("div", attrs={"data-component": "headline"})
        headline = headline_tag.get_text(strip=True) if headline_tag else "No headline"

       
        link = block.get("href")
        if link and not link.startswith("http"):
            link = urljoin("https://www.bloomberg.com", link)

       
        summary_tag = (
            block.find("section", attrs={"data-component": "summary"}) or
            block.find("div", attrs={"data-component": "summary"}) or
            block.find("p")
        )
        summary = summary_tag.get_text(strip=True) if summary_tag else get_article_summary(link)

        articles.append({
            "Headline": headline,
            "Link": link,
            "Summary": summary
        })

    driver.quit()

   
    df = pd.DataFrame(articles)
    os.makedirs("Articles", exist_ok=True)
    df.to_csv("Articles/bloomberg_articles.csv", index=False, encoding="utf-8")
    print("Saved Articles/bloomberg_articles.csv")

if __name__ == "__main__":
    scrape_bloomberg()
