# ironmen

Utility for pulling Options Market predictions.

## Setup

Install dependencies (ideally inside a virtual environment):

```bash
pip install -r requirements.txt
```

## Fetching predictions

Use the helper script to retrieve today's Options Market predictions for NVDA (or another ticker):

```bash
python scripts/fetch_predictions.py --output data/nvda_predictions.json
```

You can override the symbol, trading date, API base URL, endpoint path, and API key via flags. Set `OPTIONS_MARKET_API_KEY` in your environment if the API requires authentication.

If the live Options Market API is unreachable from your environment, you can still exercise the workflow with bundled sample data:

```bash
python scripts/fetch_predictions.py --use-sample --output data/nvda_predictions.json
```

The script will store the fetched (or sample) JSON payload in the provided output path and print its location.
