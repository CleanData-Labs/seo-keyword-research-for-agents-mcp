"""Compare a seed with its top 3 Autocomplete suggestions on one Google Trends scale.

Usage:
    pip install -r requirements.txt
    export APIFY_TOKEN=...   # Apify Console > Settings > API & Integrations
    python compare_suggestions.py

Cost: $0.004 for one seed keyword.
The run is capped with max_total_charge_usd, so it cannot cost more than $0.25.
"""
import os
import sys
from decimal import Decimal

from apify_client import ApifyClient

ACTOR_ID = "cleandata-labs/seo-keyword-research-for-agents"
MAX_COST_USD = Decimal("0.25")

RUN_INPUT = {
    "keywords": [
        "air fryer"
    ],
    "country": "GB",
    "language": "en",
    "timeRange": "today 5-y",
    "expansion": "basic",
    "compareTopSuggestions": 3
}


def run_actor(run_input: dict) -> list[dict]:
    token = os.environ.get("APIFY_TOKEN")
    if not token:
        sys.exit("Set the APIFY_TOKEN environment variable first "
                 "(Apify Console > Settings > API & Integrations).")
    client = ApifyClient(token)
    run = client.actor(ACTOR_ID).call(run_input=run_input, max_total_charge_usd=MAX_COST_USD)
    if run is None:
        sys.exit("The run could not be started.")
    print(f"Run {run.id} finished: {run.status}", file=sys.stderr)
    return list(client.dataset(run.default_dataset_id).iterate_items())


def main() -> None:
    items = run_actor(RUN_INPUT)
    for item in items:
        comparison = item.get("comparison")
        if not comparison:
            print("No comparison for", item.get("seed"), item.get("warnings") or item.get("error", ""))
            continue
        print(f"{item['seed']} in {item['geo']}, {item['timeRange']} (shared 0-100 scale)")
        for kw in comparison["keywords"]:
            print(f"  {kw:<30} average {comparison['averages'][kw]:>5}  latest {comparison['latest'][kw]:>3}  "
                  f"{comparison['directions'][kw]}")


if __name__ == "__main__":
    main()
