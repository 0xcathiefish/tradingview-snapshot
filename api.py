
import os
import uvicorn
from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv

# 唯一的依赖，就是那个我们已经验证过可以成功运行的 scraper
from tview_scraper import TradingViewScraper, TradingViewScraperError

# 加载环境变量 (.env 文件)
load_dotenv()

# --- FastAPI 应用设置 ---
app = FastAPI(
    title="Simple TradingView Chart API",
    description="A clean, minimal API that strictly follows the successful tview_scraper.py logic.",
    version="1.0.0"
)

# --- 核心 API 接口 ---
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

        # 1. 创建 Scraper 实例 (和例程一样)
        with TradingViewScraper(
            headless=True,
            chart_page_id=chart_page_id
        ) as scraper:
            
            print("Attempting to capture screenshot link...")
            # 2. 调用 get_screenshot_link() 获取原始分享链接 (和例程一样)
            raw_link = scraper.get_screenshot_link(ticker=ticker, interval=interval)
            if not raw_link:
                raise TradingViewScraperError("Scraper did not return a raw share link.")

            print(f"Raw clipboard data received: {raw_link}")
            # 3. 将原始链接转换为最终图片链接 (和例程一样)
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
        # 如果出错，返回一个标准的服务器错误
        raise HTTPException(status_code=500, detail=str(e))

# --- 健康检查接口 ---
@app.get("/")
def read_root():
    return {"status": "ok"}

# --- 启动命令 ---
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8003)
