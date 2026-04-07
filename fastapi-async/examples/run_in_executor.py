"""
run_in_executor.py
==================
How to handle CPU-bound work and legacy sync code in async FastAPI routes.

Two scenarios:
1. CPU-bound work → ProcessPoolExecutor (bypasses the GIL)
2. Legacy sync IO → asyncio.to_thread() (runs in default threadpool)

Run this file directly to see timing comparisons.
"""

import asyncio
import hashlib
import math
import time
from concurrent.futures import ProcessPoolExecutor

import uvicorn
from fastapi import FastAPI

app = FastAPI()


# ─── CPU-bound functions (run in separate processes) ──────────────────────────

def compute_primes(limit: int) -> int:
    """Count primes up to `limit` using trial division. Intentionally slow."""
    count = 0
    for n in range(2, limit):
        if all(n % i != 0 for i in range(2, int(math.sqrt(n)) + 1)):
            count += 1
    return count


def hash_repeatedly(data: str, rounds: int) -> str:
    """Hash a string many times — pure CPU work."""
    result = data.encode()
    for _ in range(rounds):
        result = hashlib.sha256(result).digest()
    return result.hex()


# ─── Legacy sync IO function (run in threadpool) ─────────────────────────────

def legacy_sync_api_call(item_id: int) -> dict:
    """
    Simulates a blocking SDK that doesn't support async.
    In reality this could be: boto3, ldap3, a SOAP client, etc.
    """
    time.sleep(1)  # simulates network latency
    return {"item_id": item_id, "data": f"result-{item_id}"}


# ─── Routes ──────────────────────────────────────────────────────────────────

# Shared process pool — create once, reuse across requests
process_pool = ProcessPoolExecutor(max_workers=4)


@app.get("/cpu/primes/{limit}")
async def count_primes(limit: int):
    """
    CPU-bound: run in a ProcessPoolExecutor.
    This keeps the event loop free while the computation runs in another process.
    """
    loop = asyncio.get_event_loop()
    count = await loop.run_in_executor(process_pool, compute_primes, limit)
    return {"limit": limit, "prime_count": count}


@app.get("/cpu/hash")
async def hash_data(data: str = "hello", rounds: int = 1_000_000):
    """
    CPU-bound hashing — offloaded to process pool.
    Without this, the event loop would be blocked for the entire duration.
    """
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(process_pool, hash_repeatedly, data, rounds)
    return {"input": data, "rounds": rounds, "hash": result}


@app.get("/legacy/item/{item_id}")
async def get_legacy_item(item_id: int):
    """
    Legacy sync SDK → use asyncio.to_thread().
    Runs the blocking function in the default threadpool.
    Simpler than run_in_executor for IO-bound sync code.
    """
    result = await asyncio.to_thread(legacy_sync_api_call, item_id)
    return result


@app.get("/legacy/items-parallel")
async def get_legacy_items_parallel():
    """
    Multiple legacy sync calls in parallel using to_thread + gather.
    Each call runs in its own thread — total time ≈ slowest call.
    """
    results = await asyncio.gather(
        asyncio.to_thread(legacy_sync_api_call, 1),
        asyncio.to_thread(legacy_sync_api_call, 2),
        asyncio.to_thread(legacy_sync_api_call, 3),
    )
    return {"items": results}


# ─── WRONG: CPU work on the event loop ───────────────────────────────────────

@app.get("/wrong/cpu-on-event-loop")
async def cpu_on_event_loop():
    """
    ANTI-PATTERN: Heavy CPU work directly in async def.
    This blocks the event loop — no other requests can be served until done.
    """
    count = compute_primes(50_000)  # ← BLOCKS the event loop
    return {"count": count}


# ─── ALSO WRONG: threads for CPU work ────────────────────────────────────────

@app.get("/wrong/cpu-in-thread")
async def cpu_in_thread():
    """
    ANTI-PATTERN: Using to_thread for CPU-bound work.
    Threads don't help CPU work because of the GIL — the thread still holds
    the GIL while computing, blocking other Python threads.
    Use ProcessPoolExecutor instead.
    """
    count = await asyncio.to_thread(compute_primes, 50_000)  # ← GIL bottleneck
    return {"count": count}


# ─── Demonstration ───────────────────────────────────────────────────────────

async def _demo():
    """Compare CPU-bound approaches."""
    limit = 1000_000

    loop = asyncio.get_event_loop()

    # Pre-warm the process pool so startup cost doesn't skew results
    pool = ProcessPoolExecutor(max_workers=4)
    await loop.run_in_executor(pool, compute_primes, 100)

    # 1. Direct — fast, but blocks the event loop (no other requests served)
    start = time.perf_counter()
    compute_primes(limit)
    direct = time.perf_counter() - start
    print(f"1. Direct (blocks loop):  {direct:.2f}s")

    # 2. Thread — same speed, but event loop stays free for other requests
    #    (however, GIL means other Python threads are still blocked)
    start = time.perf_counter()
    await asyncio.to_thread(compute_primes, limit)
    threaded = time.perf_counter() - start
    print(f"2. Thread (1 task):       {threaded:.2f}s  — same speed, loop free")

    # 3. Process pool (1 task) — similar speed, loop free, no GIL
    start = time.perf_counter()
    await loop.run_in_executor(pool, compute_primes, limit)
    process = time.perf_counter() - start
    print(f"3. Process pool (1 task): {process:.2f}s  — similar speed, loop free")

    # 4. THE REAL WIN: 4 CPU tasks in parallel across 4 cores
    #    Direct/threaded: 4x sequential = 4 * direct time
    #    Process pool:    true parallelism ≈ 1 * direct time
    print(f"\n--- Scaling test: 4 identical tasks ---")

    start = time.perf_counter()
    for _ in range(4):
        compute_primes(limit)
    direct_4x = time.perf_counter() - start
    print(f"4a. Direct 4x sequential: {direct_4x:.2f}s  (≈ 4 * {direct:.2f}s)")

    start = time.perf_counter()
    futures = [
        loop.run_in_executor(pool, compute_primes, limit)
        for _ in range(4)
    ]
    await asyncio.gather(*futures)
    parallel_4x = time.perf_counter() - start
    print(f"4b. Process pool 4x:      {parallel_4x:.2f}s  (≈ 1 * {direct:.2f}s) ← true parallelism")

    pool.shutdown(wait=False)

    # 5. Legacy sync IO via to_thread — threads shine for IO-bound work
    print(f"\n--- IO-bound: threads are ideal ---")
    start = time.perf_counter()
    await asyncio.gather(
        asyncio.to_thread(legacy_sync_api_call, 1),
        asyncio.to_thread(legacy_sync_api_call, 2),
        asyncio.to_thread(legacy_sync_api_call, 3),
    )
    legacy = time.perf_counter() - start
    print(f"5. 3x sync IO (threads):  {legacy:.2f}s  (3 * 1s calls in parallel)")


if __name__ == "__main__":
    print("=== CPU-bound & Legacy Sync Demo ===\n")
    asyncio.run(_demo())

    print("\n=== Starting FastAPI server ===")
    uvicorn.run(app, host="0.0.0.0", port=8000)
