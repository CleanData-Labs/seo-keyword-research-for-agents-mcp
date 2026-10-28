"""Print the summary, the Trends direction and the top keyword ideas for a few seed keywords.

Usage:
    pip install -r requirements.txt
    export APIFY_TOKEN=...   # Apify Console > Settings > API & Integrations
    python keyword_ideas.py

Cost: $0.004 per seed keyword (2 seeds = $0.008).
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
        "electric bike",
        "cargo bike"
    ],
    "country": "US",
    "language": "en",
    "expansion": "questions",
    "maxKeywordsPerSeed": 30
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
            print("Not researched (free):", item.get("seed"), item.get("error", ""))
            continue
        print(f"== {item['seed']} ({item['geo']})")
        print(item["summary"])
        interest = (item.get("trends") or {}).get("interest") or {}
        if interest:
            print(f"Trends: average {interest['average']}/100, direction {interest['direction']}")
        for kw in item["keywords"][:15]:
            mark = " [question]" if kw.get("isQuestion") else ""
            print(f"  - {kw['keyword']}{mark}")
        for warning in item.get("warnings") or []:
            print("  warning:", warning)
        print()


if __name__ == "__main__":
    main()
