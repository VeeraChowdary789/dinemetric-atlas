# Methodology and data quality

## Unit of analysis

One restaurant listing per Restaurant ID. All 9,551 IDs are unique, so no deduplication was necessary. Names are not unique identifiers. Filters operate on listings before aggregation.

## Preparation rules

1. Read the source as UTF-8 with an optional byte-order mark.
2. Preserve the original source file byte-for-byte.
3. Parse numeric fields and validate rating bounds and ID uniqueness.
4. Convert source rating 0 to null. Exclude nulls from rating means and minimum-rating filters.
5. Convert non-positive costs to null. Exclude nulls from medians and scatterplots.
6. Split cuisines on commas, trim whitespace and deduplicate within each restaurant.
7. Convert Yes/No delivery and booking fields to booleans.
8. Apply an explicit dataset-specific country-code lookup. It is not an ISO code table.
9. Retain damaged source text and flag affected rows; do not invent corrected names.

## Quality audit

| Check | Count | Treatment |
| --- | ---: | --- |
| Source records | 9,551 | All retained |
| Unique restaurant IDs | 9,551 | Uniqueness asserted |
| Unrated records | 2,148 | Rating set to null |
| Missing cuisines | 9 | Empty cuisine list |
| Non-positive costs | 18 | Cost set to null |
| Zero latitude/longitude pairs | 497 | Retained; no geographic map presented |
| Rows with replacement characters | 246 | Retained and flagged |

Quality counts can overlap. The damaged-text check detects the Unicode replacement character; it does not guarantee detection of every encoding issue.

## Price comparability

Source currency names are retained in exports and the explorer. Nominal costs are never averaged or compared across markets, including markets sharing a generic Dollar label. For a single selected market, the dashboard uses a country-specific display prefix. The Philippines has a suspicious Botswana Pula label and its monetary summaries are suppressed entirely. Currency labels with damaged symbols are retained in the detailed source record. No historical exchange rates are inferred.

## Visual aggregation

City and cuisine charts show the top eight groups by count. The rating distribution sums to the selected record count and includes unrated restaurants. Price-tier averages use rated listings only. The scatterplot places eligible records into 50 price bins and 30 rating bins over the full selected range. Each circle is placed at its cell's mean cost and rating. Radius grows with the square root of cell count and is capped for legibility. Full records remain available in the explorer and export.

## Interpretation

The sample is strongly concentrated in Delhi NCR. More listings do not establish greater demand, market attractiveness or profitability. Ratings are observational and may reflect selection bias. No time trends, revenue, growth, customer counts, sales forecasts or causal effects can be computed from this file. Small market samples should not be compared as if they were equally representative.
