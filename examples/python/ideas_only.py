"""Autocomplete ideas only, without Google Trends (faster and half the price), for a non-English market.

Usage:
    pip install -r requirements.txt
    export APIFY_TOKEN=...   # Apify Console > Settings > API & Integrations
    python ideas_only.py

Cost: $0.002 per seed keyword (2 seeds = $0.004).
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
        "cafea",
        "espressor"
    ],
    "country": "RO",
    "language": "ro",
    "expansion": "questions",
    "includeTrends": False,
    "maxKeywordsPerSeed": 50
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
        if item.get("type") != "keyword_research":
            continue
        ideas = [kw["keyword"] for kw in item["keywords"]]
        print(f"{item['seed']}: {len(ideas)} ideas")
        print("  " + ", ".join(ideas[:20]))


if __name__ == "__main__":
    main()
