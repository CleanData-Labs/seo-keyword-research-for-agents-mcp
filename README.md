<p align="center"><img src="assets/icon.png" alt="Keyword Research Tool — Autocomplete & Trends icon" width="96"></p>

# Keyword Research Tool — Autocomplete & Trends (remote MCP tool)

Keyword ideas from Google Autocomplete plus Google Trends interest, direction and rising searches, returned as one compact JSON result per seed keyword with a plain-English summary. No Google API key.

It runs as an [Apify Actor](https://apify.com/cleandata-labs/seo-keyword-research-for-agents) maintained by CleanData Labs, so you can use it in two ways:

1. **As a tool for your AI agent** (Claude, Cursor, VS Code / Copilot, Claude Code or any MCP client) through the hosted Apify MCP server. Nothing to install.
2. **From your own code** with the official `apify-client` for Python or JavaScript.

This repository holds the docs, ready-to-paste MCP configs and small runnable examples. The Actor itself is hosted on Apify; there is no server code to run here.

```text
https://mcp.apify.com?tools=cleandata-labs/seo-keyword-research-for-agents
```

## What it does

- **Keyword ideas from Google Autocomplete**: the seed itself, question words (what, how, why, is, can, best), modifiers (vs, for, near) and the alphabet (seed + a ... z), merged and deduplicated.
- **Google Trends for the seed**: average, latest and peak interest, overall direction (rising, falling, stable), recent momentum and a flag for spiky or seasonal interest.
- **Top and rising related searches** from Google Trends, with growth % and the "Breakout" flag.
- **Optional comparison** of the seed with up to 4 of its top suggestions on one shared Trends 0-100 scale.
- A short plain-English **`summary`** per seed that an agent can quote directly.
- Any country and language (built-in question and modifier words for English, Romanian, German, French, Spanish, Italian, Portuguese, Dutch and Polish; you can pass your own).
- **Compact** output (one JSON result per seed, small for agent context) or **flat** output (one row per keyword, for CSV and spreadsheets).

## Connect it to your AI agent (MCP)

The URL above is a Streamable HTTP MCP endpoint that exposes one tool, `cleandata-labs--seo-keyword-research-for-agents`, whose arguments are the [input fields](docs/input-reference.md). Two ways to authorize:

- **OAuth (recommended):** add only the URL. On first use your client opens an Apify sign-in page. A free Apify account works.
- **API token:** send the header `Authorization: Bearer <YOUR_APIFY_TOKEN>`. Get the token in [Apify Console > Settings > API & Integrations](https://console.apify.com/settings/integrations). Keep it out of git.

Ready-made config files are in [`examples/mcp/`](examples/mcp/).

### Claude (claude.ai and Claude Desktop)

Settings > Connectors > **Add custom connector**. Name: `Keyword Research`, Remote MCP server URL: `https://mcp.apify.com?tools=cleandata-labs/seo-keyword-research-for-agents`. Sign in with Apify when asked.

If you prefer a local config file, Claude Desktop can run Apify's official stdio server instead (`claude_desktop_config.json`, needs Node.js 18+):

```json
{
  "mcpServers": {
    "keyword-research": {
      "command": "npx",
      "args": ["-y", "@apify/actors-mcp-server", "--tools", "cleandata-labs/seo-keyword-research-for-agents"],
      "env": { "APIFY_TOKEN": "<YOUR_APIFY_TOKEN>" }
    }
  }
}
```

### Cursor

`~/.cursor/mcp.json` (global) or `.cursor/mcp.json` (project). OAuth:

```json
{
  "mcpServers": {
    "keyword-research": {
      "url": "https://mcp.apify.com?tools=cleandata-labs/seo-keyword-research-for-agents"
    }
  }
}
```

With a token instead:

```json
{
  "mcpServers": {
    "keyword-research": {
      "url": "https://mcp.apify.com?tools=cleandata-labs/seo-keyword-research-for-agents",
      "headers": { "Authorization": "Bearer <YOUR_APIFY_TOKEN>" }
    }
  }
}
```

### VS Code (GitHub Copilot agent mode)

`.vscode/mcp.json`. OAuth:

```json
{
  "servers": {
    "keyword-research": {
      "type": "http",
      "url": "https://mcp.apify.com?tools=cleandata-labs/seo-keyword-research-for-agents"
    }
  }
}
```

With a token, VS Code can prompt for it once and store it securely:

```json
{
  "inputs": [
    { "type": "promptString", "id": "apify-token", "description": "Apify API token", "password": true }
  ],
  "servers": {
    "keyword-research": {
      "type": "http",
      "url": "https://mcp.apify.com?tools=cleandata-labs/seo-keyword-research-for-agents",
      "headers": { "Authorization": "Bearer ${input:apify-token}" }
    }
  }
}
```

### Claude Code

```bash
claude mcp add --transport http keyword-research "https://mcp.apify.com?tools=cleandata-labs/seo-keyword-research-for-agents"
# or with a token:
claude mcp add --transport http keyword-research "https://mcp.apify.com?tools=cleandata-labs/seo-keyword-research-for-agents" --header "Authorization: Bearer $APIFY_TOKEN"
```

### Other clients and combining tools

Any client that supports remote Streamable HTTP servers can use the same URL. To load several Actors in one connection, separate them with commas, e.g. `https://mcp.apify.com?tools=cleandata-labs/seo-keyword-research-for-agents,cleandata-labs/google-trends-explorer`. Already using `https://mcp.apify.com` with the default tools? Ask your agent to run `cleandata-labs/seo-keyword-research-for-agents`.

### Try these prompts

- "Use the keyword research tool for 'electric bike' in the US. Is interest growing, and which questions do people ask most?"
- "Find keyword ideas for 'cafea' in Romania (language ro) and list the 10 most useful ones for a coffee shop blog."
- "Compare 'air fryer' with its top 3 suggestions on Google Trends in the UK over the past 5 years."

### Tips for agents

- Smallest useful input: `{"keywords": ["electric bike"], "country": "US"}` (one result, $0.004).
- Always pass your own `keywords`; the default `["electric bike"]` is only a demo.
- One seed with the default `expansion: "full"` usually takes 20-40 seconds, longer if Google slows down Trends. For a quicker answer use `expansion: "questions"` or `"basic"`, or `includeTrends: false`.
- Quote the `summary` field, then use `keywords` for details: filter `isQuestion: true` for FAQ and content ideas, and `trendsRisingPercent` / `isBreakout` for what is growing.
- Keep `maxKeywordsPerSeed` around 30-50 if context space matters.
- Trends values are relative interest (0-100), not search volume. Say so when you report them. The tool does not return search volume, CPC or keyword difficulty.

## Use it from code

Python (`pip install apify-client`):

```python
import os
from apify_client import ApifyClient

client = ApifyClient(os.environ["APIFY_TOKEN"])
run = client.actor("cleandata-labs/seo-keyword-research-for-agents").call(run_input={"keywords": ["electric bike"], "country": "US", "expansion": "questions", "maxKeywordsPerSeed": 30})
for item in client.dataset(run.default_dataset_id).iterate_items():
    print(item)
```

JavaScript / Node.js (`npm install apify-client`):

```js
import { ApifyClient } from 'apify-client';

const client = new ApifyClient({ token: process.env.APIFY_TOKEN });
const run = await client.actor('cleandata-labs/seo-keyword-research-for-agents').call({"keywords": ["electric bike"], "country": "US", "expansion": "questions", "maxKeywordsPerSeed": 30});
const { items } = await client.dataset(run.defaultDatasetId).listItems();
console.log(items);
```

Runnable examples, each with a hard cost cap (`max_total_charge_usd` / `maxTotalChargeUsd`):

- Python: [`keyword_ideas.py`](examples/python/keyword_ideas.py), [`questions_to_csv.py`](examples/python/questions_to_csv.py), [`compare_suggestions.py`](examples/python/compare_suggestions.py), [`ideas_only.py`](examples/python/ideas_only.py). See [`examples/python/README.md`](examples/python/README.md).
- Node.js: [`keyword-ideas.mjs`](examples/node/keyword-ideas.mjs), [`rising-searches.mjs`](examples/node/rising-searches.mjs). See [`examples/node/README.md`](examples/node/README.md).

```bash
export APIFY_TOKEN=...            # never commit it
cd examples/python && pip install -r requirements.txt && python keyword_ideas.py
cd examples/node && npm install && node keyword-ideas.mjs
```

You can also call it over plain HTTP, from Make, Zapier or n8n, or on a schedule. See the [Apify API docs](https://docs.apify.com/api/v2).

## Input and output

Full list of input fields with types and defaults: [`docs/input-reference.md`](docs/input-reference.md).

Example output row:

```json
{
  "type": "keyword_research",
  "seed": "electric bike",
  "geo": "US",
  "language": "en",
  "timeRange": "today 12-m",
  "expansion": "full",
  "summary": "\"electric bike\" (US, past 12 months): Google Trends interest trended up over the period (+34% fitted change); average 30.8/100, latest 13/100, peak in the period starting 2026-04-12. Recent momentum is down (-66% for the latest quarter of the period vs the quarter before). ...",
  "trends": {
    "status": "ok",
    "interest": {
      "average": 30.8,
      "latest": 13,
      "latestDate": "2026-10-18",
      "peak": 100,
      "peakDate": "2026-04-12",
      "low": 10,
      "direction": "rising",
      "trendChangePercent": 34,
      "recentChangePercent": -66,
      "recentMomentum": "down",
      "slopePerPoint": 0.208,
      "pointCount": 52,
      "isSpiky": true
    },
    "topQueries": [
      {
        "query": "electric dirt bike",
        "value": 100
      }
    ],
    "risingQueries": [
      {
        "query": "electric mini bike",
        "growthPercent": 300,
        "isBreakout": false
      }
    ],
    "trendsUrl": "https://trends.google.com/trends/explore?q=electric%20bike&date=today%2012-m&geo=US"
  },
  "comparison": null,
  "keywordCount": 100,
  "keywordsFoundBeforeCap": 360,
  "autocompleteIdeaCount": 73,
  "questionCount": 50,
  "keywords": [
    {
      "keyword": "electric bike",
      "sources": [
        "seed",
        "autocomplete"
      ],
      "foundVia": "seed",
      "autocompletePosition": 1,
      "isQuestion": false,
      "wordCount": 2,
      "trendsAverage": 30.8,
      "trendsLatest": 13,
      "trendsDirection": "rising"
    },
    {
      "keyword": "what electric bikes are street legal",
      "sources": [
        "autocomplete"
      ],
      "foundVia": "prefix:what",
      "autocompletePosition": 1,
      "isQuestion": true,
      "wordCount": 6
    },
    {
      "keyword": "electric bike for kids",
      "sources": [
        "autocomplete",
        "trends_top",
        "trends_rising"
      ],
      "foundVia": "seed",
      "autocompletePosition": 2,
      "isQuestion": false,
      "wordCount": 4,
      "trendsTopValue": 22,
      "trendsRisingPercent": 80
    }
  ],
  "warnings": [],
  "note": "Trends values are relative interest (0-100, 100 = peak in this period/location), not search volumes.",
  "dataSources": [
    "google_autocomplete",
    "google_trends"
  ],
  "scrapedAt": "2026-10-28T17:24:40+00:00"
}
```

Shortened: `keywords` normally holds up to `maxKeywordsPerSeed` entries (the seed first, then Autocomplete ideas in the order found, then queries only Google Trends returned). Each keyword can have `keyword`, `sources` (`seed`, `autocomplete`, `trends_top`, `trends_rising`), `foundVia` (e.g. `prefix:how`, `suffix:vs`, `alphabet:a`), `autocompletePosition`, `isQuestion`, `wordCount`, `trendsTopValue`, `trendsRisingPercent`, `isBreakout` and, for the seed or compared keywords, `trendsAverage` / `trendsLatest` / `trendsDirection`; in compact mode empty optional fields are left out. `trends.status` is `ok`, `no_data`, `failed` or `skipped`. With `compareTopSuggestions` > 0, `comparison` holds `keywords`, `averages`, `latest` and `directions` on one shared scale. With `outputMode: "flat"` you get one `type: "keyword"` row per keyword with the same field names plus `seed`, `rank`, `seedAverage`, `seedLatest`, `seedDirection` and `seedTrendChangePercent`. Failed seeds come back as free `type: "error"` rows.

## Pricing

Pay per event on Apify: **$0.004 per seed keyword** ($4 per 1,000 seeds): $0.002 for the keyword ideas plus $0.002 for the Google Trends insights. You pay Apify from your own Apify account; nothing is billed through this repository.

- Each seed is charged once, however many keyword ideas it returns. The flat output mode (one row per keyword) costs the same as compact.
- If Google Trends fails or returns nothing for a seed, you pay only the $0.002 for the ideas. With `includeTrends: false` a seed costs $0.002 (ideas only).
- Error rows and seeds with no data at all are free.
- Apify adds its standard Actor start event ($0.00005 per run). There is no separate compute or proxy fee.
- The smallest *maximum cost per run* you can set for this Actor is $0.25. The Actor checks the limit before each seed and stops cleanly when it is reached.

Apify's free plan includes a monthly platform credit (currently $5), which is enough to try the tool on real data. Prices can change; the [Actor page](https://apify.com/cleandata-labs/seo-keyword-research-for-agents) always shows the current price.

## Good to know

- This is an independent tool by CleanData Labs. It is not affiliated with or endorsed by Google. It reads publicly available pages; use the data in line with the source site's terms and the laws that apply to you.
- The examples call the live Actor, so each run costs a little (see the cost note at the top of each script).
- Found a bug or need a field? Open an issue here or on the Actor's Issues tab on Apify.

## Links

- Apify Actor: <https://apify.com/cleandata-labs/seo-keyword-research-for-agents>
- MCP endpoint: `https://mcp.apify.com?tools=cleandata-labs/seo-keyword-research-for-agents`
- MCP registry name: `io.github.CleanData-Labs/seo-keyword-research-for-agents` (see [`server.json`](server.json))
- Apify MCP server docs: <https://docs.apify.com/platform/integrations/mcp>

More tools from CleanData Labs:

- [Google Trends Scraper](https://github.com/CleanData-Labs/google-trends-explorer-mcp): Google Trends data for AI agents and scripts: interest over time, interest by region, related and rising queries, Trending Now and keyword suggestions.
- [URL to Markdown Converter](https://github.com/CleanData-Labs/url-to-markdown-mcp): Turn web pages and PDFs into clean, LLM-ready Markdown with metadata, token counts and optional RAG chunks.
- [Google Ads Transparency Scraper](https://github.com/CleanData-Labs/google-ads-transparency-explorer-mcp): See the ads any company runs on Google Search, YouTube, Shopping, Maps and Play, from the public Google Ads Transparency Center.

## License

The example code and docs in this repository are released under the [MIT License](LICENSE). The hosted Actor is a paid service under [Apify's terms](https://apify.com/store-terms-and-conditions).
