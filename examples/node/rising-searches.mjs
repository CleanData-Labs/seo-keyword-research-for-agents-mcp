// List the rising Google Trends searches and breakout keywords for a seed.
//
// Usage:
//   npm install
//   export APIFY_TOKEN=...   # Apify Console > Settings > API & Integrations
//   node rising-searches.mjs
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
  "expansion": "basic"
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

for (const item of items.filter((i) => i.type === 'keyword_research')) {
  console.log(`${item.seed} (${item.geo}): Trends status ${item.trends.status}`);
  for (const q of item.trends.risingQueries ?? []) {
    const growth = q.isBreakout ? 'Breakout' : `+${q.growthPercent}%`;
    console.log(`  ${q.query.padEnd(35)} ${growth}`);
  }
}
