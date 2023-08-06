import json
import duckdb

from datetime import datetime

from typing import List, Dict, Any


def iso8601_to_timestamp(input_str: str) -> int:
    date_str, _ = input_str.split(".", 1)   # for now, ignore timezone
    print( date_str)
    return int(datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S").timestamp())


TIMELINE_KEYS = {
    "id": int,
    "created_at": iso8601_to_timestamp,
    "url": str,
    "replies_count": int,
    "reblogs_count": int,
    "favourites_count": int,
}

TYPE_CONVERSIONS = {
    int: "INT64",
    str: "VARCHAR",
}

def timeline_to_parquet(timeline: List[Dict[str, Any]]) -> None:

    con = duckdb.connect(database=':memory:')
    print("L=", len( timeline[0].keys()))
    toots = []
    for post in timeline:
        toots.append(tuple(v(post[k]) for k, v in TIMELINE_KEYS.items()))

    if len(toots) < 1:
        return

    table_items = ", ".join(tuple(f"{key} {TYPE_CONVERSIONS[type(toots[0][idx])]}" for idx, key in enumerate( list(TIMELINE_KEYS.keys()))))
    # print(table_items)
    # print( toots )
    # create a table
    con.execute(f"CREATE TABLE items({table_items})")
    con.executemany("INSERT INTO items VALUES (?, ?, ?, ?, ?, ?)", toots )

    # retrieve the items again
    con.execute("SELECT * FROM items")
    for item in con.fetchall():
        print(item)

    con.execute("COPY (SELECT * FROM items) TO 'result-snappy.parquet' (FORMAT 'parquet')")
    # con.execute("EXPORT DATABASE 'target_directory' (FORMAT PARQUET)")
    # print( timeline[0].keys() )
    # print('#'*50)
    # del timeline[0]["account"]
    # print(json.dumps(timeline, indent=4, default=str))
