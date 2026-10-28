# Node.js examples

Needs Node.js 18+ and an Apify API token.

```bash
npm install
export APIFY_TOKEN=...   # Apify Console > Settings > API & Integrations
node keyword-ideas.mjs
```

| Script | What it does | Cost |
|---|---|---|
| `keyword-ideas.mjs` | Print the summary and the top keyword ideas for a seed keyword. | $0.004 per seed keyword. |
| `rising-searches.mjs` | List the rising Google Trends searches and breakout keywords for a seed. | $0.004 per seed keyword. |

Every script sets `maxTotalChargeUsd`, so a run stops before it can cost more than the cap. Files are written to `./output/` (git-ignored).
