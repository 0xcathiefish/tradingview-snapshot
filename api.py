import os
import uvicorn
from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv

# The only dependency is the scraper we've already verified works.
from tview_scraper import TradingViewScraper, TradingViewScraperError

# Load environment variables (from .env file)
load_dotenv()

# --- FastAPI App Setup ---
app = FastAPI(
    title="Simple TradingView Chart API",
    description="A clean, minimal API that strictly follows the successful tview_scraper.py logic.",
    version="1.0.0"
)

# --- Core API Endpoint ---
@app.get("/chart")
def get_chart(ticker: str, interval: str):
    """
    This endpoint's logic is a direct copy of the successful execution path
    from the tview_scraper.py example script.
    """
    print(f"--- Clean API request received for {ticker} ({interval}) ---")
    
    chart_page_id = os.getenv("MCP_SCRAPER_CHART_PAGE_ID") or None
    
    try:
        # ====================================================================
        #  vvv   THIS IS THE EXACT LOGIC FROM THE SUCCESSFUL EXAMPLE   vvv
        # ====================================================================

        # 1. Create a Scraper instance (same as the example)
        with TradingViewScraper(
            headless=True,
            chart_page_id=chart_page_id
        ) as scraper:
            
            print("Attempting to capture screenshot link...")
            # 2. Call get_screenshot_link() to get the raw share link (same as the example)
            raw_link = scraper.get_screenshot_link(ticker=ticker, interval=interval)
            if not raw_link:
                raise TradingViewScraperError("Scraper did not return a raw share link.")

            print(f"Raw clipboard data received: {raw_link}")
            # 3. Convert the raw link to the final image link (same as the example)
            #image_url = scraper.convert_link_to_image_url(raw_link)
            image_url = raw_link
            if not image_url:
                 raise TradingViewScraperError("Failed to convert raw share link to an image URL.")

        # ====================================================================
        #  ^^^                END OF COPIED LOGIC                ^^^
        # ====================================================================
        
        print(f"Success! Final Image Link: {image_url}")
        return {"ticker": ticker, "interval": interval, "image_url": image_url}

    except Exception as e:
        print(f"An error occurred: {e}")
        # If an error occurs, return a standard server error
        raise HTTPException(status_code=500, detail=str(e))

# --- Health Check Endpoint ---
@app.get("/")
def read_root():
    return {"status": "ok"}

# --- Startup Command ---
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8003)