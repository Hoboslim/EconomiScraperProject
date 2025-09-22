import pandas as pd
import subprocess
import time
import os
import json

def run_classification():
    try:
        df = pd.read_csv(os.path.join("Articles", "cnbc_articles.csv"))
    except Exception as e:
        print(f"Error: Could not read CSV file.\n{e}")
        return

    rows = []
    total = min(len(df), 50)
    print(f"Processing {total} articles...\n")

    for i, row in df.iterrows():
        if i >= total:
            break

        text = row.get("Summary", "")
        if text == "No summary" or not str(text).strip():
            text = row.get("Headline", "")

        headline = row.get("Headline", "")
        link = row.get("Link", "")

        print(f"Processing article {i+1}/{total}...")

        prompt = f"""
You are a news classifier. Analyze the following article and return results in JSON format with exactly these keys:
- category: ONE category (e.g., Politics, Business, Health, Technology, Culture, Sports, etc.)
- sentiment: Neutral, Positive, or Negative
- summary: A very short 1–2 sentence summary in English

Article:
{text}

Return ONLY valid JSON.
"""

        t0 = time.time()
        try:
            result = subprocess.run(
                ["ollama", "run", "gemma3:12b", prompt],
                capture_output=True,
                text=True,
                encoding="utf-8",
                timeout=60
            )
            response = result.stdout.strip()
        except Exception as e:
            response = "{\"category\": \"ERROR\", \"sentiment\": \"ERROR\", \"summary\": \"Error occurred\"}"
            print(f"Error processing article {i+1}: {e}")

        t1 = time.time()

       
        try:
            parsed = json.loads(response)
            category = parsed.get("category", "Unknown")
            sentiment = parsed.get("sentiment", "Unknown")
            summary = parsed.get("summary", "")
        except Exception:
            category = "ParseError"
            sentiment = "ParseError"
            summary = response[:200]

        rows.append({
            "Headline": headline,
            "Link": link,
            "Model_Category": category,
            "Sentiment": sentiment,
            "Model_Summary": summary,
            "Time (s)": round(t1 - t0, 2)
        })

   
    all_summaries = [row["Model_Summary"] for row in rows if row.get("Model_Summary")]

    overview_prompt = f"""
You are an economic analyst. Based on the following article summaries,
write a short overview (3–5 sentences) about the current economic situation:

- How is the economy looking (growth, slowdown, stability)?
- Is it likely to improve or get worse in the near future?
- How is unemployment trending (getting better or worse)?

Summaries:
{all_summaries}

Return only plain text.
"""

    try:
        result = subprocess.run(
            ["ollama", "run", "gemma3:12b", overview_prompt],
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=120
        )
        economic_overview = result.stdout.strip()
    except Exception as e:
        economic_overview = f"Error generating overview: {e}"

    
    rows.append({
        "Headline": "Economic Overview",
        "Link": "",
        "Model_Category": "Overview",
        "Sentiment": "N/A",
        "Model_Summary": economic_overview,
        "Time (s)": 0
    })

   
    results_df = pd.DataFrame(rows)
    os.makedirs("ClassificationResults", exist_ok=True)
    per_article_file = os.path.join("ClassificationResults", "per_article_results.csv")
    results_df.to_csv(per_article_file, index=False, encoding="utf-8")
    print(f"Results saved to {per_article_file}")


if __name__ == "__main__":
    run_classification()
