"""Pull ETF daily flow data from Farside Investors and save as CSV."""

import urllib.request
import re
import csv
from datetime import datetime

OUT = "memories/mev/physics/data/etf_daily_flows.csv"

URLS = {
    "btc": "https://farside.co.uk/bitcoin-etf-flow-all-data/",
    "eth": "https://farside.co.uk/ethereum-etf-flow-all-data/",
}


def fetch_page(url):
    req = urllib.request.Request(url, headers={
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
    })
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read().decode('utf-8')


def parse_flow_value(s):
    """Parse a flow value like '263.2', '(89.3)', '-', '' into float (millions USD).
    Parentheses = negative. '-' or '' = 0."""
    s = s.strip().replace(',', '')
    if not s or s == '-':
        return 0.0
    negative = '(' in s
    s = s.replace('(', '').replace(')', '')
    try:
        val = float(s)
        return -val if negative else val
    except ValueError:
        return 0.0


def parse_date(s):
    """Parse '11 Jan 2024' → '2024-01-11'."""
    try:
        dt = datetime.strptime(s.strip(), '%d %b %Y')
        return dt.strftime('%Y-%m-%d')
    except ValueError:
        return None


def extract_total_flows(html):
    """Extract date and Total column from Farside HTML table."""
    tables = re.findall(r'<table[^>]*>(.*?)</table>', html, re.DOTALL)
    # Find table with most rows
    table = max(tables, key=lambda t: len(re.findall(r'<tr', t)))
    rows = re.findall(r'<tr[^>]*>(.*?)</tr>', table, re.DOTALL)

    flows = {}
    for row in rows:
        cells = re.findall(r'<t[hd][^>]*>(.*?)</t[hd]>', row, re.DOTALL)
        cell_texts = [re.sub(r'<[^>]+>', '', c).strip().replace('&nbsp;', '').strip() for c in cells]
        # Filter to non-empty cells
        clean = [c for c in cell_texts if c.strip()]

        if not clean:
            continue

        date = parse_date(clean[0])
        if date is None:
            continue

        # Total is always the last numeric column
        # The last clean value should be the Total
        total = parse_flow_value(clean[-1])
        flows[date] = total

    return flows


def main():
    # Pull BTC flows
    print("Fetching BTC ETF flows...")
    btc_html = fetch_page(URLS["btc"])
    btc_flows = extract_total_flows(btc_html)
    print(f"  BTC dates: {len(btc_flows)} ({min(btc_flows)} to {max(btc_flows)})")

    # Pull ETH flows
    print("Fetching ETH ETF flows...")
    eth_html = fetch_page(URLS["eth"])
    eth_flows = extract_total_flows(eth_html)
    print(f"  ETH dates: {len(eth_flows)} ({min(eth_flows)} to {max(eth_flows)})")

    # Merge into single CSV
    all_dates = sorted(set(btc_flows.keys()) | set(eth_flows.keys()))
    print(f"Total unique dates: {len(all_dates)}")

    with open(OUT, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['date', 'btc_flow_usd_m', 'eth_flow_usd_m'])
        for date in all_dates:
            btc = btc_flows.get(date, '')
            eth = eth_flows.get(date, '')
            writer.writerow([date,
                           f'{btc:.1f}' if isinstance(btc, float) else '',
                           f'{eth:.1f}' if isinstance(eth, float) else ''])

    print(f"Saved {OUT}")

    # Verification
    import pandas as pd
    df = pd.read_csv(OUT)
    print(f"\nVerification:")
    print(f"  Rows: {len(df)}")
    print(f"  BTC flow range: {df['btc_flow_usd_m'].min():.1f} to {df['btc_flow_usd_m'].max():.1f} M")
    print(f"  ETH flow range: {df['eth_flow_usd_m'].min():.1f} to {df['eth_flow_usd_m'].max():.1f} M")
    print(f"\n  Sample:")
    print(df.head(5).to_string())
    print(f"\n  Recent:")
    print(df.tail(5).to_string())


if __name__ == "__main__":
    main()
