# Python examples

Needs Python 3.10+ and an Apify API token.

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export APIFY_TOKEN=...   # Apify Console > Settings > API & Integrations
python keyword_ideas.py
```

| Script | What it does | Cost |
|---|---|---|
| `keyword_ideas.py` | Print the summary, the Trends direction and the top keyword ideas for a few seed keywords. | $0.004 per seed keyword (2 seeds = $0.008). |
| `questions_to_csv.py` | Collect question-style keywords for several seeds into a CSV file (flat output mode). | $0.004 per seed keyword (3 seeds = $0.012). |
| `compare_suggestions.py` | Compare a seed with its top 3 Autocomplete suggestions on one Google Trends scale. | $0.004 for one seed keyword. |
| `ideas_only.py` | Autocomplete ideas only, without Google Trends (faster and half the price), for a non-English market. | $0.002 per seed keyword (2 seeds = $0.004). |

Every script sets `max_total_charge_usd`, so a run stops before it can cost more than the cap. Files are written to `./output/` (git-ignored).
