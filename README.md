# TradingView Chart Image API

A simple FastAPI HTTP server and Docker support for fetching TradingView chart images.

## Features

- **Chart Image API:** Fetches TradingView chart images via a simple HTTP endpoint.
- **FastAPI Server:** Exposes the scraping functionality via a `/chart` HTTP endpoint for easy integration.
- **Dockerized Deployment:** Includes `Dockerfile` and `docker-compose.yml` for quick and consistent setup.
- **Environment Configuration:** Fully configurable via environment variables.
- **Secure Authentication:** Uses session-based authentication for TradingView.

## Setup

1.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
2.  **Configure Environment:**
    - Copy `.env.example` to `.env`.
    - Fill in your `TRADINGVIEW_SESSION_ID` and `TRADINGVIEW_SESSION_ID_SIGN` in the `.env` file. You can obtain these from your browser's cookies after logging into TradingView.
    - This `.env` file is used when running the server.

## Running the API Server

### With Uvicorn

1.  **Run the API Server:**
    ```bash
    # Make sure your .env file is configured with your credentials
    uvicorn api:app --host 0.0.0.0 --port 8003
    ```

### With Docker

For easy and consistent deployment, this project includes a `Dockerfile` and `docker-compose.yml`.

1.  **Configure Environment:**
    Copy `.env.example` to `.env` and fill in your TradingView session credentials. The `docker-compose.yml` file is configured to pass these variables to the container.

2.  **Build and Run the Container:**
    ```bash
    # This will build the image and start the API service in the background
    docker compose up -d --build
    ```
    The API will be available at `http://localhost:8003`.

3.  **Stopping the Service:**
    ```bash
    docker compose down
    ```

## API Documentation

### Endpoint: `GET /chart`

**Query Parameters:**
- `ticker` (str): The TradingView ticker symbol (e.g., "BYBIT:BTCUSDT.P"). **Required**.
- `interval` (str): The chart time interval. **Required**. This must be a string representing minutes (e.g., '1', '5', '60'), or 'D' for daily, 'W' for weekly. For example, `1h` is not valid; use `60` instead.

**Example Usage (with curl):**
```bash
curl "http://localhost:8003/chart?ticker=NASDAQ:AAPL&interval=60"

curl "http://localhost:8003/chart?ticker=BYBIT:BTCUSDT.P&interval=240"
```

**Success Response (JSON):**
```json
{
  "ticker": "NASDAQ:AAPL",
  "interval": "60",
  "image_url": "data:image/png;base64,...",
  "png_url": "https://s3.tradingview.com/snapshots/..."
}
```

## Configuration

### Environment Variables

The following environment variables can be set in your `.env` file to configure the scraper:

- `TRADINGVIEW_SESSION_ID`: Your TradingView session ID (required)
- `TRADINGVIEW_SESSION_ID_SIGN`: Your TradingView session ID signature (required)
- `MCP_SCRAPER_HEADLESS`: Run browser in headless mode (default: `True`)
- `MCP_SCRAPER_WINDOW_WIDTH`: Browser window width (default: `1920`)
- `MCP_SCRAPER_WINDOW_HEIGHT`: Browser window height (default: `1080`)
- `MCP_SCRAPER_USE_SAVE_SHORTCUT`: Use clipboard image capture instead of screenshot links (default: `True`)
- `MCP_SCRAPER_CHART_PAGE_ID`: Custom chart page ID (optional)
