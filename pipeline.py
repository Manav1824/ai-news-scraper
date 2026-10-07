import os
import time
import requests
from bs4 import BeautifulSoup
from google import genai
from google.genai import types

def run_pipeline():
    # --- PHASE 1: DATA EXTRACTION (Web Scraping) ---
    url = 'https://news.ycombinator.com/'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    print(f"Scraping live data from {url}...")
    
    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Grab the top 10 tech headlines
    headline_elements = soup.find_all('span', class_='titleline')
    headlines = [el.a.text for el in headline_elements[:10]]
    
    print(f"Successfully scraped {len(headlines)} headlines.")
    print("Handing off to Gemini AI for market analysis...")

    # --- PHASE 2: AI ENRICHMENT (Gemini API) ---
    try:
        client = genai.Client()
    except Exception as e:
        print("Error: Could not initialize client. Check your GEMINI_API_KEY.")
        return

    system_instruction = (
        "You are an expert technology analyst. Read the provided news headlines and "
        "return a JSON array. For each headline, create an object containing: "
        "'headline' (the exact text), 'primary_topic' (e.g., AI, Cybersecurity, Business, Software), "
        "and 'market_impact' (High, Medium, or Low)."
    )
    prompt = f"Live Headlines:\n{headlines}"

    # The Professional Retry Loop
    max_retries = 3
    api_response = None
    
    for attempt in range(max_retries):
        try:
            print(f"Contacting Gemini (Attempt {attempt + 1}/{max_retries})...")
            api_response = client.models.generate_content(
                model="gemini-3.8-flash",
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    response_mime_type="application/json"
                )
            )
            break # If successful, break out of the retry loop
            
        except Exception as e:
            if "503" in str(e):
                print("Google servers are busy. Waiting 5 seconds to retry...")
                time.sleep(5)
            else:
                print(f"An unexpected API error occurred: {e}")
                return

    if not api_response:
        print("Failed to reach Gemini after multiple attempts. Please try again later.")
        return

    # --- PHASE 3: DATA STORAGE ---
    filename = 'enriched_market_intel.json'
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(api_response.text)
        
    print(f"\nSuccess! End-to-end pipeline complete.")
    print(f"Structured AI data successfully saved to {filename}")

if __name__ == '__main__':
    run_pipeline()