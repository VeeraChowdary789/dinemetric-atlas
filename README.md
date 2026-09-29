# DineMetric Atlas

A complete restaurant analytics portfolio project built from a supplied 9,551-row Zomato dataset. Explore listing supply, ratings, cuisine mix, price tiers and service availability through an interactive dashboard. The analysis defaults to India and supports all 15 represented markets.

## Run the dashboard

Open **`dist/index.html`** in a modern browser. No installation, API key or internet connection is required. Keep its three neighboring files (`styles.css`, `analytics.js`, `app.js`) and `data.js` alongside it.

Alternatively, with Python 3 installed:

```bash
python3 -m http.server 8000 --directory dist
```

Then open `http://localhost:8000`.

## Dashboard features

- Six metrics: restaurant count, average rating, median cost for two, delivery availability, booking availability and votes.
- Market, city, cuisine, price tier, delivery and minimum-rating filters, plus text search.
- City supply ranking, rating distribution, cuisine mix, binned price-versus-rating scatterplot and price-tier comparison.
- Restaurant explorer with sorting, pagination and CSV export of the complete filtered selection.
- Visible metric definitions, quality audit and source limitations.
- Responsive layout, keyboard-operable controls and a skip-navigation link.
- CSV exports escape spreadsheet formula prefixes.

## Verified findings

| Measure | India sample |
| --- | ---: |
| Restaurants | 8,652 |
| Represented cities | 43 |
| Rated restaurants | 6,513 |
| Average rating, rated listings only | 3.352 / 5 |
| Median positive cost for two | ₹450 |
| Restaurants offering online delivery | 2,423 (28.0%) |
| Restaurants offering table booking | 1,111 (12.8%) |
| Recorded votes | 1,187,163 |

New Delhi contributes 5,473 listings (63.3% of the India sample). North Indian is the most frequently listed cuisine (3,946 restaurants). These describe the supplied sample, not national market share.

## Project layout

```text
dist/                    Offline-capable interactive dashboard
data/raw/zomato.csv       Original supplied dataset, unchanged
data/processed/           Cleaned CSV, SQLite database, audit JSON
scripts/prepare_data.py  Reproducible preparation pipeline (Python stdlib)
sql/market_analysis.sql  Analytical SQLite queries
tests/analytics.test.cjs Independent control totals and metric edge cases
powerbi/                 Theme, DAX measures and reconstruction guide
docs/                    Findings, data dictionary and methodology
.github/workflows/       Automated validation on pushes and pull requests
```

## Reproduce the analysis

Requirements: Python 3.10+ and Node.js 20+ for tests. There are no third-party runtime dependencies.

```bash
python3 scripts/prepare_data.py
node --test tests/*.test.cjs
node --check dist/app.js
```

The pipeline validates unique IDs, parses numeric and boolean fields, splits cuisines and writes the dashboard payload, cleaned CSV, SQLite tables and quality report. It stops on duplicate IDs or ratings outside 0–5 instead of silently discarding data. Replacing the source with a different snapshot requires reviewing and updating the snapshot-specific expected control totals in the tests.

SQL queries can run in DB Browser for SQLite or with:

```bash
sqlite3 -header -column data/processed/zomato.sqlite < sql/market_analysis.sql
```

## Analytical choices

Zero ratings are treated as **unrated**, not as poor ratings. Non-positive costs become unavailable. Monetary comparisons are restricted to one market; the Philippines is excluded from price aggregation because its source currency is labeled Botswana Pula. No currency conversion is attempted. Cuisine totals overlap by design. The scatterplot bins all eligible records rather than presenting an undisclosed sample.

The file contains no collection date, transactions or sales figures. Votes are not customers or orders. Service availability is not utilization. See [methodology](docs/methodology.md) for additional limitations.

## Power BI

The `powerbi` directory contains a JSON theme, DAX measures and step-by-step setup instructions using the processed CSV. It is a reconstruction starter, **not a generated `.pbix` file**. Native Power BI rendering and DAX execution were not tested in Power BI Desktop.

## Project links

- Repository: https://github.com/VeeraChowdary789/dinemetric-atlas
- Hosted dashboard (owner access): https://dinemetric-atlas.pvchowdary44.chatgpt.site
- Offline dashboard: open `dist/index.html` after downloading or cloning this repository.

## Validation

Six automated tests pass, including source totals, unrated handling, mixed-currency suppression, combined filtering, empty results and rating-distribution reconciliation. SQLite queries independently confirm India counts, rating and median cost. JavaScript syntax and local asset references were checked. Browser visual testing and native WebMCP validation were unavailable in the execution environment; responsive behavior has not been visually verified. The optional WebMCP selection reader feature-detects support and does not affect ordinary dashboard use.

## Source and attribution

Source: user-supplied **Zomato Restaurant Dataset.csv**. Its collection date, original publisher and redistribution license were not provided. No license is asserted over the source dataset. The original bytes and SHA-256 digest are retained for traceability. This independent portfolio project is not affiliated with Zomato.
