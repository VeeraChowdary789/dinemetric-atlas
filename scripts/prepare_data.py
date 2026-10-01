"""Reproduce the dashboard dataset, SQLite database and audit using Python stdlib."""
import csv
import hashlib
import json
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COUNTRIES = {1: 'India', 14: 'Australia', 30: 'Brazil', 37: 'Canada', 94: 'Indonesia', 148: 'New Zealand', 162: 'Philippines', 166: 'Qatar', 184: 'Singapore', 189: 'South Africa', 191: 'Sri Lanka', 208: 'Turkey', 214: 'United Arab Emirates', 215: 'United Kingdom', 216: 'United States'}

def prepare():
    source = ROOT / 'data/raw/zomato.csv'
    with source.open(encoding='utf-8-sig', newline='') as f:
        raw = list(csv.DictReader(f))
    records = []
    ids = set()
    for row in raw:
        rid = int(row['Restaurant ID'])
        if rid in ids:
            raise ValueError(f'Duplicate restaurant ID: {rid}; resolve before publishing')
        ids.add(rid)
        rating, cost = float(row['Aggregate rating']), float(row['Average Cost for two'])
        country = int(row['Country Code'])
        if not 0 <= rating <= 5:
            raise ValueError(f'Invalid rating for {rid}')
        cuisines = sorted(set(c.strip() for c in row['Cuisines'].split(',') if c.strip()))
        records.append(dict(id=rid, name=row['Restaurant Name'].strip(), country=country,
            market=COUNTRIES.get(country, f'Market {country}'), city=row['City'].strip(),
            locality=row['Locality'].strip(), cuisines=cuisines,
            cost=cost if cost > 0 else None, currency=row['Currency'].strip(),
            priceRange=int(row['Price range']), rating=rating if rating > 0 else None,
            votes=int(row['Votes']), booking=row['Has Table booking']=='Yes',
            delivery=row['Has Online delivery']=='Yes',
            latitude=float(row['Latitude']), longitude=float(row['Longitude']),
            textIssue=any('\ufffd' in value for value in row.values())))
    audit = dict(sourceRows=len(raw), uniqueRestaurants=len(ids),
        unrated=sum(r['rating'] is None for r in records),
        missingCuisines=sum(not r['cuisines'] for r in records),
        nonPositiveCost=sum(r['cost'] is None for r in records),
        zeroCoordinates=sum(r['latitude']==0 and r['longitude']==0 for r in records),
        encodingAffectedRows=sum(r['textIssue'] for r in records),
        sourceSHA256=hashlib.sha256(source.read_bytes()).hexdigest(),
        source='User-supplied Zomato Restaurant Dataset.csv',
        snapshotDate=None,
        countries=COUNTRIES)
    payload = dict(records=records, audit=audit)
    for directory in ['dist', 'data/processed']:
        (ROOT/directory).mkdir(parents=True, exist_ok=True)
    (ROOT/'dist/data.js').write_text('window.ZOMATO_DATA = '+json.dumps(payload,ensure_ascii=True,separators=(',',':'))+';\n')
    (ROOT/'data/processed/audit.json').write_text(json.dumps(audit,indent=2)+'\n')
    columns=list(records[0])
    with (ROOT/'data/processed/restaurants.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=columns);w.writeheader()
        for record in records:
            w.writerow({**record,'cuisines':'; '.join(record['cuisines'])})
    db=sqlite3.connect(ROOT/'data/processed/zomato.sqlite')
    db.executescript('DROP TABLE IF EXISTS restaurant_cuisines; DROP TABLE IF EXISTS restaurants; CREATE TABLE restaurants (id INTEGER PRIMARY KEY, name TEXT, country INTEGER, market TEXT, city TEXT, locality TEXT, cost REAL, currency TEXT, price_range INTEGER, rating REAL, votes INTEGER, booking INTEGER, delivery INTEGER, text_issue INTEGER); CREATE TABLE restaurant_cuisines (restaurant_id INTEGER, cuisine TEXT, PRIMARY KEY(restaurant_id,cuisine), FOREIGN KEY(restaurant_id) REFERENCES restaurants(id));')
    db.executemany('INSERT INTO restaurants VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)',[(r['id'],r['name'],r['country'],r['market'],r['city'],r['locality'],r['cost'],r['currency'],r['priceRange'],r['rating'],r['votes'],r['booking'],r['delivery'],r['textIssue']) for r in records])
    db.executemany('INSERT INTO restaurant_cuisines VALUES (?,?)',[(r['id'],c) for r in records for c in r['cuisines']])
    db.commit();db.close()
    print(json.dumps(audit,indent=2))
    return records,audit

if __name__=='__main__': prepare()
