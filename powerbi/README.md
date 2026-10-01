# Rebuild in Power BI Desktop

This folder is a Power BI starter. A native PBIX is not included, and these measures have not been executed in Power BI Desktop.

1. Import `data/processed/restaurants.csv` using Get data → Text/CSV. Name the query **Restaurants**.
2. In Power Query, set `id`, `country`, `priceRange`, `votes` to Whole Number; `cost`, `rating`, `latitude`, `longitude` to Decimal Number; `delivery`, `booking`, `textIssue` to True/False. Preserve missing rating and cost values as null.
3. Create measures from `measures.dax`, **one at a time**. Format rate measures as percentages with one decimal place and Average Rating as 0.00. Leave cost numeric when using multiple markets; use an INR format only on an India-only page.
4. Import `dinemetric-atlas-theme.json` from View → Themes → Browse for themes.
5. Make a 16:9 report page with six cards: Total Restaurants, Average Rating, Median Cost for Two, Online Delivery %, Table Booking %, Total Votes.
6. Add market, city, priceRange and delivery slicers. Default market to India. Use a single-select market slicer for price charts and exclude country 162 from monetary charts.
7. Add a city bar chart, rating histogram (with a separate unrated count), a cost-versus-rating scatter chart, a priceRange comparison and an explorer table. Configure rating and cost axes/aggregations explicitly; do not sum ratings.
8. For cuisines, reference Restaurants in Power Query, keep `id` and `cuisines`, split `cuisines` by semicolon **into rows**, trim, remove empty values and deduplicate id/cuisine pairs. Name it RestaurantCuisines. Use DISTINCTCOUNT(RestaurantCuisines[id]) for the cuisine chart. If enabling a cuisine slicer to filter Restaurants, use a carefully reviewed relationship/filter design and validate counts against the web dashboard.
9. Add a methodology page with the quality audit and notes from `docs/methodology.md`.
10. Verify the India control totals in the main README before saving your PBIX.

Suggested visual design: page background #F5F6F8, white panels, #CF3448 highlights, dark #23191F navigation, teal #287F72 for cuisine/quality comparisons. Keep titles short and place units beside metrics.
