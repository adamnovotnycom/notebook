import requests

YAHOO_FINANCE_CHART_URL = "https://query1.finance.yahoo.com/v8/finance/chart/AAPL"


def get_apple_price() -> float:
    """Return the most recent trading price of Apple (AAPL) stock via the Yahoo Finance API."""
    response = requests.get(
        YAHOO_FINANCE_CHART_URL,
        params={"interval": "1d", "range": "1d"},
        headers={"User-Agent": "Mozilla/5.0"},
    )
    response.raise_for_status()
    data = response.json()
    return data["chart"]["result"][0]["meta"]["regularMarketPrice"]


if __name__ == "__main__":
    print(get_apple_price())
