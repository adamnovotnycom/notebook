#!/usr/bin/env python3
"""Print Apple's latest regular-session quote and quarterly revenue from Yahoo Finance.

Uses only Python's standard library. Quotes may be delayed; outside trading
hours the price is the latest regular-session price.
"""

import json
import sys
from datetime import datetime, timedelta, timezone
from urllib.error import URLError
from urllib.request import Request, urlopen


def fetch_json(url):
    request = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urlopen(request, timeout=15) as response:
        return json.load(response)


def latest_quarterly_revenue():
    now = datetime.now(timezone.utc)
    start = int((now - timedelta(days=730)).timestamp())
    end = int((now + timedelta(days=1)).timestamp())
    url = (
        "https://query1.finance.yahoo.com/ws/fundamentals-timeseries/v1/finance/timeseries/AAPL"
        f"?type=quarterlyTotalRevenue&period1={start}&period2={end}"
    )
    series = fetch_json(url)["timeseries"]
    if series.get("error"):
        raise ValueError(str(series["error"]))
    quarters = [
        entry
        for result in (series.get("result") or [])
        for entry in (result.get("quarterlyTotalRevenue") or [])
        if entry and entry.get("periodType") == "3M"
        and entry.get("reportedValue", {}).get("raw") is not None
    ]
    if not quarters:
        raise ValueError("Yahoo Finance returned no quarterly revenue data")
    latest = max(quarters, key=lambda entry: entry["asOfDate"])
    return latest["reportedValue"]["raw"], latest["currencyCode"], latest["asOfDate"]


def main():
    url = "https://query1.finance.yahoo.com/v8/finance/chart/AAPL?interval=1d&range=1d"
    try:
        chart = fetch_json(url)["chart"]
        if chart.get("error"):
            raise ValueError(str(chart["error"]))
        quote = chart["result"][0]["meta"]
        price = float(quote["regularMarketPrice"])
        currency = quote["currency"]
        timestamp = datetime.fromtimestamp(quote["regularMarketTime"], timezone.utc)
    except (URLError, OSError, ValueError, KeyError, IndexError, TypeError) as exc:
        print(f"Could not fetch Apple's stock price: {exc}", file=sys.stderr)
        return 1

    print(f"Apple (AAPL): {price:.2f} {currency}")
    print(f"As of {timestamp:%Y-%m-%d %H:%M:%S UTC} (regular session; may be delayed)")
    try:
        revenue, revenue_currency, quarter_end = latest_quarterly_revenue()
        print(f"Latest quarterly revenue: {revenue:,.0f} {revenue_currency}")
        print(f"Quarter ended {quarter_end}")
    except (URLError, OSError, ValueError, KeyError, IndexError, TypeError) as exc:
        print(f"Could not fetch Apple's quarterly revenue: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
