# Input reference: Keyword Research for AI Agents

Generated from the Actor's published input schema. All fields are optional unless marked required. The same fields are the arguments of the MCP tool `cleandata-labs--seo-keyword-research-for-agents`.

Live version: <https://apify.com/cleandata-labs/seo-keyword-research-for-agents/input-schema>

| Field | Type | Default | Description |
|---|---|---|---|
| `keywords` **(required)** | array | `["electric bike"]` | Short search phrases to research, one result per phrase. Example: ["electric bike", "cargo bike"]. Max 100 per run; duplicates are ignored. |
| `country` | string | `"US"` | 2-letter country code for Autocomplete and Trends. Example: "US", "GB" ("UK" also works), "DE", "RO". Use "" for worldwide. Default "US". |
| `language` | string | `"en"` | Language code for suggestions and question words. Example: "en", "ro", "de", "pt-BR". Default "en". Match it to the country for best results. |
| `timeRange` | string: `now 7-d` / `today 1-m` / `today 3-m` / `today 12-m` / `today 5-y` / `all` | `"today 12-m"` | Period for the Google Trends interest summary. Default "today 12-m" (past 12 months). Use "today 5-y" to see seasonality over several years. |
| `customTimeRange` | string |  | Optional exact period that overrides timeRange. Format "YYYY-MM-DD YYYY-MM-DD", e.g. "2025-01-01 2025-12-31". |
| `expansion` | string: `basic` / `questions` / `full` | `"full"` | How many Autocomplete lookups per seed. "basic" = the seed itself; "questions" = also what/how/why/is/can/best + seed and seed + vs/for/near; "full" (default) = also seed + a ... z. Deeper = more ideas, slower. Price is the same. |
| `includeTrends` | boolean | `true` | true (default) = add Google Trends interest (average, latest, peak, direction) and top + rising related queries. false = Autocomplete ideas only (faster, cheaper). |
| `compareTopSuggestions` | integer (min 0, max 4) | `0` | 0-4. Compare the seed with this many top Autocomplete ideas on one shared Trends 0-100 scale, to see which variant people search most. Default 0 (off). Adds 2 Trends requests per seed. |
| `maxKeywordsPerSeed` | integer (min 5, max 500) | `100` | Cap on the merged keyword list per seed (5-500). Default 100. Lower it to keep agent context small; Trends queries are always kept. |
| `outputMode` | string: `compact` / `flat` | `"compact"` | "compact" (default) = one result per seed with a summary and a nested keyword list. "flat" = one dataset row per keyword with the same field names, for CSV. Price is the same. |
| `questionPrefixes` | array |  | Optional. Replaces the built-in question words put before the seed. Example: ["how to", "what is", "best"]. Built-in lists exist for en, ro, de, fr, es, it, pt, nl, pl. |
| `modifierSuffixes` | array |  | Optional. Replaces the built-in words put after the seed. Example: ["vs", "for", "near me", "price"]. |
| `autocompleteDelaySecs` | integer (min 0, max 10) | `0` | Extra pause between Autocomplete lookups in seconds, 0-10. Default 0 (a built-in ~0.3 s polite pause always applies). |
| `delayBetweenRequestsSecs` | integer (min 0, max 30) | `1` | Pause between Google Trends requests in seconds, 0-30. Default 1. Raise it if you see many retries in the log. |
| `maxRetries` | integer (min 0, max 10) | `3` | Retries on rate limits or network errors, 0-10. Default 3. Each retry uses a new session (and a new proxy IP). |
| `requestTimeoutSecs` | integer (min 5, max 120) | `30` | Timeout per HTTP request in seconds, 5-120. Default 30. |
| `proxyConfiguration` | object | `{"useApifyProxy": true}` | Default {"useApifyProxy": true} (recommended: Google rate-limits busy IPs and retries rotate the IP). If the proxy is refused, the run continues without it. |
