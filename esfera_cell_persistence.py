"""Staging-only transactional persistence for planned cell tasks."""
import os
from uuid import UUID
from esfera_cell_queue import plan_task
from esfera_ops import connection, backend, record

def enqueue_review_task(kind, offer_slug, idempotency_key):
    if os.getenv("ESFERA_ENV","development") not in ("test","development","staging"):
        raise RuntimeError("Task enqueue disabled outside nonproduction environments")
    task=plan_task(kind,offer_slug,idempotency_key)
    pg=backend()
    if pg != "postgres":
        raise RuntimeError("Staging queue requires PostgreSQL and migration 003")
    with connection() as db:
        row=db.execute(
            """INSERT INTO esfera_cell_tasks
              (id,idempotency_key,offer_slug,kind,target_cell,status,external_actions_enabled)
              VALUES (%s,%s,%s,%s,%s,'REVIEW_REQUIRED',FALSE)
              ON CONFLICT (idempotency_key) DO NOTHING RETURNING id""",
            (UUID(task["id"]),task["idempotency_key"],task["offer_slug"],
             task["kind"],task["target_cell"])).fetchone()
        if row is None:
            existing=db.execute(
                "SELECT kind,offer_slug,target_cell,status FROM esfera_cell_tasks WHERE idempotency_key=%s",
                (idempotency_key,)).fetchone()
            if not existing or existing[0]!=kind or existing[1]!=offer_slug:
                raise ValueError("Idempotency key already used for another task")
            return {"created":False,"status":existing[3],"external_actions_enabled":False}
    record("CELL_TASK_REVIEW_QUEUED",{"kind":kind,"offer_slug":offer_slug,
                                     "target_cell":task["target_cell"]})
    return {"created":True,"status":"REVIEW_REQUIRED","target_cell":task["target_cell"],
            "external_actions_enabled":False}
