# ⚡ End-to-End AI Web Scraping Pipeline

An automated data pipeline that extracts live web data and processes it through a Large Language Model for real-time categorization and enrichment. 

## Workflow
1. **Extraction:** Uses `requests` and `BeautifulSoup` to scrape live text from target URLs.
2. **AI Enrichment:** Feeds raw text directly into Google's `gemini-3.8-flash` model.
3. **Structuring:** Enforces a rigid JSON schema via system instructions to extract market impact and topic categories.
4. **Storage:** Automatically exports the structured intelligence to a local JSON database.

*Built to demonstrate full-stack automation, from unstructured web HTML to machine-readable AI insights.*