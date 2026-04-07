"""
route_sync_vs_async.py
======================
When to use `def` vs `async def` for FastAPI route handlers.

FastAPI treats them differently:
- `def`       → runs in a threadpool (won't block the event loop)
- `async def` → runs directly on the event loop (MUST use await, never block)

The decision tree:
  Is your route doing async IO (awaiting something)?
  ├── YES → async def + await
  └── NO  → plain def (FastAPI's threadpool keeps things safe)

Run this file to see timing comparisons, then start the server to test routes.
"""

import asyncio
import time

import httpx
import uvicorn
from fastapi import FastAPI

app = FastAPI()


# ─── 1. Plain def — correct for sync work ────────────────────────────────────

@app.get("/sync/config")
def get_config():
    """
    No IO, no computation — just returns data.
    Plain def is the right choice. FastAPI runs it in a threadpool,
    but for simple returns it barely matters.
    """
    return {"version": "1.0", "debug": False}


@app.get("/sync/blocking-io")
def sync_blocking_io():
    """
    Sync blocking call in a plain def — SAFE.
    FastAPI runs def routes in a threadpool, so time.sleep here does NOT
    freeze the event loop. Other async routes keep serving requests.

    Use this pattern for: sync DB drivers, legacy SDKs, file I/O with open().
    """
    time.sleep(1)  # runs in thread — event loop stays free
    return {"waited": "1s", "event_loop": "was free the whole time"}


# ─── 2. async def — correct for async IO ─────────────────────────────────────

@app.get("/async/single-call")
async def async_single_call():
    """
    async def + async library = correct.
    httpx yields control at every await, letting the event loop serve
    other requests while waiting for the response.
    """
    async with httpx.AsyncClient() as client:
        response = await client.get("https://httpbin.org/delay/1")
    return {"status": response.status_code}


@app.get("/async/parallel-calls")
async def async_parallel_calls():
    """
    Multiple async IO calls run concurrently with gather.
    Total time ≈ max(individual times), not sum.
    """
    async with httpx.AsyncClient() as client:
        r1, r2 = await asyncio.gather(
            client.get("https://httpbin.org/delay/1"),
            client.get("https://httpbin.org/delay/2"),
        )
    return {
        "call_1": r1.status_code,
        "call_2": r2.status_code,
        "note": "took ~2s total, not 3s",
    }


# ─── 3. WRONG — blocking calls inside async def ──────────────────────────────

@app.get("/wrong/blocking-sleep-in-async")
async def wrong_blocking_sleep():
    """
    ANTI-PATTERN: time.sleep in async def freezes the ENTIRE event loop.
    While sleeping, no other request — sync or async — can be processed.
    """
    time.sleep(2)  # ← FREEZES EVERYTHING
    return {"problem": "all other requests were blocked for 2s"}


@app.get("/wrong/sync-http-in-async")
async def wrong_sync_http():
    """
    ANTI-PATTERN: requests (sync HTTP) in async def blocks the event loop.
    Use httpx.AsyncClient or wrap with asyncio.to_thread().
    """
    import requests  # noqa
    response = requests.get("https://httpbin.org/delay/1")  # ← BLOCKS
    return {"status": response.status_code}


# ─── 4. Edge case — async def that doesn't await anything ────────────────────

@app.get("/edge/async-no-await")
async def async_no_await():
    """
    This works but is pointless — if you're not awaiting anything,
    use plain def instead. async def without await just adds overhead
    (the coroutine wrapper) with no benefit.
    """
    return {"tip": "use plain def if you have nothing to await"}


# ─── 5. Mixed — sync helper wrapped with to_thread ───────────────────────────

def _slow_sync_computation(n: int) -> int:
    """
    Simulates a sync-only library call with no async alternative.
    Think: boto3, ldap3, a legacy SOAP client, subprocess, etc.
    The busy loop represents real CPU/IO work inside the library.
    """
    # Simulate ~1s of work with no async equivalent
    deadline = time.perf_counter() + 1.0
    while time.perf_counter() < deadline:
        pass
    return n * 2


@app.get("/mixed/sync-in-async")
async def mixed_sync_in_async(n: int = 21):
    """
    When you need async def (e.g., for other awaits in the same route)
    but also call a sync function — wrap it with to_thread.
    """
    result = await asyncio.to_thread(_slow_sync_computation, n)
    return {"input": n, "result": result}


# ─── Decision Reference ─────────────────────────────────────────────────────
#
# ┌─────────────────────────────────┬────────────┬─────────────────────────────┐
# │ Scenario                        │ Use        │ Why                         │
# ├─────────────────────────────────┼────────────┼─────────────────────────────┤
# │ No IO at all                    │ def        │ Simplest, no overhead       │
# │ Sync DB (psycopg2, pymysql)     │ def        │ Threadpool keeps loop free  │
# │ Async DB (asyncpg, aiosqlite)   │ async def  │ Must await the queries      │
# │ Async HTTP (httpx, aiohttp)     │ async def  │ Must await the responses    │
# │ Legacy sync SDK                 │ def        │ Or async def + to_thread    │
# │ Mix of sync + async             │ async def  │ Wrap sync parts in to_thread│
# └─────────────────────────────────┴────────────┴─────────────────────────────┘


# ─── Demonstration ───────────────────────────────────────────────────────────

async def _demo():
    """Show the difference between sequential and concurrent awaits."""
    print("Sequential awaits (1s + 2s = 3s):")
    start = time.perf_counter()
    await asyncio.sleep(1)
    await asyncio.sleep(2)
    print(f"  Elapsed: {time.perf_counter() - start:.2f}s\n")

    print("Concurrent with create_task (max(1s, 2s) = 2s):")
    start = time.perf_counter()
    t1 = asyncio.create_task(asyncio.sleep(1))  # scheduled NOW
    t2 = asyncio.create_task(asyncio.sleep(2))  # scheduled NOW
    await t1  # both already running in parallel
    await t2
    print(f"  Elapsed: {time.perf_counter() - start:.2f}s\n")

    print("Concurrent with gather (same thing, cleaner syntax):")
    start = time.perf_counter()
    await asyncio.gather(asyncio.sleep(1), asyncio.sleep(2))
    print(f"  Elapsed: {time.perf_counter() - start:.2f}s\n")

    print("to_thread: sync work + async work in parallel (max(1s, 0.5s) = 1s):")
    start = time.perf_counter()
    sync_result, async_result = await asyncio.gather(
        asyncio.to_thread(_slow_sync_computation, 21),  # 1s sync, in thread
        asyncio.sleep(0.5),                              # 0.5s async, on loop
    )
    print(f"  Result: {sync_result}, elapsed: {time.perf_counter() - start:.2f}s")
    print(f"  (sync + async ran in parallel — loop was free during sync work)\n")

    print("Without to_thread: sync blocks the loop (1s + 0.5s = 1.5s):")
    start = time.perf_counter()
    _slow_sync_computation(21)  # 1s sync, blocks the loop
    await asyncio.sleep(0.5)    # 0.5s async, can only start after sync finishes
    print(f"  Elapsed: {time.perf_counter() - start:.2f}s")
    print(f"  (sync blocked the loop — async sleep had to wait)\n")


if __name__ == "__main__":
    print("=== def vs async def Demo ===\n")
    asyncio.run(_demo())

    print("=== Starting FastAPI server ===")
    uvicorn.run(app, host="0.0.0.0", port=8000)
