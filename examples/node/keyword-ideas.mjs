// Print the summary and the top keyword ideas for a seed keyword.
//
// Usage:
//   npm install
//   export APIFY_TOKEN=...   # Apify Console > Settings > API & Integrations
//   node keyword-ideas.mjs
//
// Cost: $0.004 per seed keyword.
// The run is capped with maxTotalChargeUsd, so it cannot cost more than $0.25.
import { ApifyClient } from 'apify-client';

const ACTOR_ID = 'cleandata-labs/seo-keyword-research-for-agents';
const MAX_COST_USD = 0.25;

const input = {
  "keywords": [
    "electric bike"
  ],
  "country": "US",
  "language": "en",
  "expansion": "questions",
  "maxKeywordsPerSeed": 30
};

const token = process.env.APIFY_TOKEN;
if (!token) {
  console.error('Set the APIFY_TOKEN environment variable first (Apify Console > Settings > API & Integrations).');
  process.exit(1);
}

const client = new ApifyClient({ token });
const run = await client.actor(ACTOR_ID).call(input, { maxTotalChargeUsd: MAX_COST_USD });
console.error(`Run ${run.id} finished: ${run.status}`);
const { items } = await client.dataset(run.defaultDatasetId).listItems();

for (const item of items) {
  if (item.type !== 'keyword_research') {
    console.log(`Not researched (free): ${item.seed ?? ''} ${item.error ?? ''}`);
    continue;
  }
  console.log(`== ${item.seed} (${item.geo})`);
  console.log(item.summary);
  for (const kw of item.keywords.slice(0, 15)) {
    console.log(`  - ${kw.keyword}${kw.isQuestion ? ' [question]' : ''}`);
  }
}
