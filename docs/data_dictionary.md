# Processed data dictionary

| Field | Type | Meaning |
| --- | --- | --- |
| id | Integer | Unique source Restaurant ID |
| name | Text | Source restaurant name, whitespace trimmed |
| country | Integer | Dataset-specific country code |
| market | Text | Country label from project lookup |
| city | Text | Source city |
| locality | Text | Source neighborhood or location |
| cuisines | List / semicolon-separated CSV text | Distinct trimmed cuisines |
| cost | Nullable number | Positive source average cost for two |
| currency | Text | Uncorrected source currency label |
| priceRange | Integer | Source price category, 1–4 |
| rating | Nullable number | Source rating greater than zero, out of 5 |
| votes | Integer | Source recorded rating votes |
| booking | Boolean | Source table-booking availability |
| delivery | Boolean | Source online-delivery availability |
| latitude / longitude | Number | Source coordinates, including invalid zero pairs |
| textIssue | Boolean | A source field contains a replacement character |

SQLite uses `price_range` and `text_issue` rather than camelCase. It normalizes cuisines into `restaurant_cuisines(restaurant_id, cuisine)`. Geographic coordinates are kept in the cleaned CSV/dashboard payload but omitted from SQLite because this analysis does not use mapping.
