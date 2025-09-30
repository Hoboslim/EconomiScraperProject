import pandas as pd
import subprocess
import time
import os
import json

def run_classification(file_path):
    # Load input CSV
    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        print(f"Error: Could not read CSV file.\n{e}")
        return

    
    input_name = os.path.splitext(os.path.basename(file_path))[0]  
    output_folder = os.path.join("ClassificationResults")
    os.makedirs(output_folder, exist_ok=True)


    timestamp = time.strftime("%Y%m%d_%H%M%S")
    output_file = os.path.join(output_folder, f"{input_name}_classification_{timestamp}.csv")
    
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
            print(f"Error processing article {i+1}: {e}")
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
    results_df.to_csv(output_file, index=False, encoding="utf-8")
    print(f"Results saved to {output_file}")


if __name__ == "__main__":
    
    input_file = "Articles/bloomberg_articles.csv"  
    run_classification(input_file)
