"""Authenticated operator import service; writes only PENDING_REVIEW offers."""
from esfera_hotmart import validate_batch
from esfera_ops import connection, backend, record

def import_offers(items):
    rows = validate_batch(items)
    pg = backend() == "postgres"
    table = "esfera_hotmart_offers"
    # Schema migration 002 must be applied explicitly before this operation.
    sql = (f"INSERT INTO {table} (slug,title,hotlink,status,partner_verified,"
           "link_destination_verified,attribution_verified,publish_enabled) "
           f"VALUES ({','.join(['%s' if pg else '?']*8)})")
    # Fail closed on duplicate or missing table; no overwrite of approved offers.
    with connection() as db:
        for row in rows:
            db.execute(sql, (row["slug"],row["title"],row["hotlink"],"PENDING_REVIEW",
                             False,False,False,False))
    record("HOTMART_IMPORT_PENDING_REVIEW", {"slugs":[row["slug"] for row in rows], "count":len(rows)})
    return {"imported":len(rows), "status":"PENDING_REVIEW", "publication_allowed":False}
