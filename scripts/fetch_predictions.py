import argparse
import datetime as dt
import json
import os
from pathlib import Path
from typing import Any, Dict, Optional

import requests


DEFAULT_BASE_URL = "https://api.options.market"
DEFAULT_PREDICTION_PATH = "/v1/predictions"
DEFAULT_SYMBOL = "NVDA"
SAMPLE_PATH = Path("sample_data/options_market_nvda_prediction_sample.json")


def _coerce_date_string(date: Optional[str]) -> str:
    if date:
        return date
    return dt.date.today().isoformat()


def fetch_predictions(
    symbol: str = DEFAULT_SYMBOL,
    date: Optional[str] = None,
    *,
    base_url: str = DEFAULT_BASE_URL,
    prediction_path: str = DEFAULT_PREDICTION_PATH,
    api_key: Optional[str] = None,
    session: Optional[requests.Session] = None,
) -> Dict[str, Any]:
    request_session = session or requests.Session()
    params = {"ticker": symbol.upper(), "date": _coerce_date_string(date)}
    headers = {}

    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    url = f"{base_url.rstrip('/')}{prediction_path}"
    response = request_session.get(url, params=params, headers=headers, timeout=20)
    response.raise_for_status()
    return response.json()


def load_sample_predictions() -> Dict[str, Any]:
    with SAMPLE_PATH.open() as handle:
        return json.load(handle)


def save_json(payload: Dict[str, Any], destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(payload, indent=2, sort_keys=True))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Fetch today's Options Market predictions for NVDA (or another symbol)."
    )
    parser.add_argument(
        "--symbol",
        default=DEFAULT_SYMBOL,
        help="Ticker symbol to request (default: NVDA)",
    )
    parser.add_argument(
        "--date",
        help="Target trading date in YYYY-MM-DD (default: today)",
    )
    parser.add_argument(
        "--base-url",
        default=DEFAULT_BASE_URL,
        help="Base URL for the Options Market API.",
    )
    parser.add_argument(
        "--prediction-path",
        default=DEFAULT_PREDICTION_PATH,
        help="Path for the predictions endpoint (appended to base URL).",
    )
    parser.add_argument(
        "--api-key",
        default=os.getenv("OPTIONS_MARKET_API_KEY"),
        help="API key for authenticated requests.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("data/nvda_predictions.json"),
        help="Where to store the response JSON.",
    )
    parser.add_argument(
        "--use-sample",
        action="store_true",
        help="Use bundled sample data instead of making a live network request.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if args.use_sample:
        predictions = load_sample_predictions()
    else:
        predictions = fetch_predictions(
            symbol=args.symbol,
            date=args.date,
            base_url=args.base_url,
            prediction_path=args.prediction_path,
            api_key=args.api_key,
        )

    save_json(predictions, args.output)
    print(f"Saved predictions for {args.symbol.upper()} to {args.output}")


if __name__ == "__main__":
    main()
