import pandas as pd
import subprocess
import time
import os
import json
import re
from datetime import datetime

def run_classification(file_path, model_name="gemma3:12b"):
    try:
        df_articles = pd.read_csv(file_path)
        if "Classified" not in df_articles.columns:
            df_articles["Classified"] = False
        else:
            df_articles["Classified"] = df_articles["Classified"].astype(bool)
    except Exception as e:
        print(f"Error: Could not read CSV file.\n{e}")
        return

    unclassified_df = df_articles[df_articles["Classified"] == False]

    if unclassified_df.empty:
        print("All articles are already classified!")
        return

    base_name = os.path.splitext(os.path.basename(file_path))[0]
    base_name = re.sub(r"\d+$", "", base_name)
    if base_name.endswith("_articles"):
        source_name = base_name.replace("_articles", "")
    else:
        source_name = base_name

    output_folder = os.path.join("ClassificationResults")
    os.makedirs(output_folder, exist_ok=True)
    output_file = os.path.join(output_folder, f"{source_name}_classification.csv")

    rows = []
    total = len(unclassified_df)
    print(f"Processing {total} new articles...\n")

    for idx, row in unclassified_df.iterrows():
        text = row.get("Summary", "")
        if text == "No summary" or not str(text).strip():
            text = row.get("Headline", "")

        headline = row.get("Headline", "")
        link = row.get("Link", "")

        date_str = row.get("Date") or row.get("Published") or datetime.now().strftime("%Y-%m-%d")
        text_with_date = f"[{date_str}] {text}"

        print(f"Processing article {idx+1}/{total}...")

        prompt = f"""
You are a news classifier. Analyze the following article and return results in JSON format with exactly these keys:
- category: ONE category (e.g., Politics, Business, Health, Technology, Culture, Sports, etc.)
- sentiment: Neutral, Positive, or Negative
- summary: A very short 1–2 sentence summary in English

Article:
{text_with_date}

Return ONLY valid JSON.
"""

        t0 = time.time()
        try:
            result = subprocess.run(
                ["ollama", "run", model_name, prompt],
                capture_output=True,
                text=True,
                encoding="utf-8",
                timeout=60
            )
            response = result.stdout.strip()
        except Exception as e:
            print(f"Error processing article {idx+1}: {e}")
            response = '{"category": "ERROR", "sentiment": "ERROR", "summary": "Error occurred"}'

        t1 = time.time()

        clean_response = response.strip()
        if clean_response.startswith("```json"):
            clean_response = clean_response[len("```json"):].strip()
        if clean_response.startswith("```"):
            clean_response = clean_response[len("```"):].strip()
        if clean_response.endswith("```"):
            clean_response = clean_response[:-3].strip()

        try:
            parsed = json.loads(clean_response)
            category = parsed.get("category", "Unknown")
            sentiment = parsed.get("sentiment", "Unknown")
            summary = parsed.get("summary", "No summary")
        except Exception:
            category = "ParseError"
            sentiment = "ParseError"
            summary = "Error processing article"

        summary_with_date = f"[{date_str}] {summary}"

        rows.append({
            "Headline": headline,
            "Link": link,
            "Model_Category": category,
            "Sentiment": sentiment,
            "Model_Summary": summary_with_date,
            "Time (s)": round(t1 - t0, 2),
            "Classified": True
        })

        df_articles.loc[idx, "Classified"] = True

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
            ["ollama", "run", model_name, overview_prompt],
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
        "Time (s)": 0,
        "Classified": True
    })

    results_df = pd.DataFrame(rows)
    if os.path.exists(output_file):
        df_existing = pd.read_csv(output_file)
        results_df = pd.concat([df_existing, results_df], ignore_index=True)
        results_df = results_df.drop_duplicates(subset=["Headline", "Link"], keep="first")
    results_df.to_csv(output_file, index=False, encoding="utf-8")

    print(f"Results saved to {output_file}")

    df_articles.to_csv(file_path, index=False, encoding="utf-8")
    print(f"Updated original CSV: {file_path}")


if __name__ == "__main__":
    input_file = "Articles/aftonbladet_articles.csv"
    run_classification(input_file)
