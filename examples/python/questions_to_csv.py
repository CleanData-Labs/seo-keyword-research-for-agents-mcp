"""Collect question-style keywords for several seeds into a CSV file (flat output mode).

Usage:
    pip install -r requirements.txt
    export APIFY_TOKEN=...   # Apify Console > Settings > API & Integrations
    python questions_to_csv.py

Cost: $0.004 per seed keyword (3 seeds = $0.012).
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
        "air fryer",
        "standing desk",
        "electric bike"
    ],
    "country": "US",
    "language": "en",
    "expansion": "full",
    "maxKeywordsPerSeed": 100,
    "outputMode": "flat"
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
    import csv

    rows = [i for i in items if i.get("type") == "keyword" and i.get("isQuestion")]
    os.makedirs("output", exist_ok=True)
    path = os.path.join("output", "questions.csv")
    fields = ["seed", "rank", "keyword", "foundVia", "autocompletePosition", "wordCount", "seedDirection"]
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows)} question keywords to {path}")


if __name__ == "__main__":
    main()
