"""
common_mistakes.py
==================
Anti-patterns in async FastAPI code — each with an explanation and fix.

These are the mistakes that cause "my async FastAPI app is slow" or
"requests are timing out" issues. Each section shows the wrong way,
explains WHY it's wrong, and provides the correct approach.

This file is runnable as a FastAPI app to demonstrate the differences.
"""

import asyncio
import time
from concurrent.futures import ProcessPoolExecutor

import httpx
import uvicorn
from fastapi import BackgroundTasks, FastAPI

app = FastAPI()


# ─── Mistake 1: Blocking sleep in async def ──────────────────────────────────

@app.get("/mistake/1-blocking-sleep")
async def mistake_blocking_sleep():
    """
    WRONG: time.sleep() in async def blocks the entire event loop.
    While sleeping, NO other request can be processed — not even fast ones.

    Root cause: async def runs on the event loop thread. time.sleep() is a
    blocking call that doesn't yield control back to the loop.
    """
    time.sleep(2)  # ← BLOCKS ALL REQUESTS FOR 2 SECONDS
    return {"status": "done"}


@app.get("/fix/1-async-sleep")
async def fix_async_sleep():
    """
    FIX: Use asyncio.sleep() — it yields control back to the event loop,
    allowing other requests to be served while this one waits.
    """
    await asyncio.sleep(2)  # ← event loop serves other requests during this
    return {"status": "done"}


# ─── Mistake 2: Sync HTTP client in async def ────────────────────────────────

@app.get("/mistake/2-sync-http")
async def mistake_sync_http():
    """
    WRONG: Using `requests` (sync) inside async def blocks the event loop
    for the entire duration of the HTTP call.

    The `requests` library does not support async. It blocks on socket I/O.
    """
    import requests  # noqa
    response = requests.get("https://httpbin.org/delay/1")  # ← BLOCKS
    return {"status": response.status_code}


@app.get("/fix/2-async-http")
async def fix_async_http():
    """
    FIX: Use httpx.AsyncClient (or aiohttp) — these yield at await points,
    keeping the event loop responsive.
    """
    async with httpx.AsyncClient() as client:
        response = await client.get("https://httpbin.org/delay/1")
    return {"status": response.status_code}


# ─── Mistake 3: Sequential awaits instead of concurrent ──────────────────────

async def _fetch_slow(label: str, seconds: float) -> str:
    await asyncio.sleep(seconds)
    return f"{label}: done"


@app.get("/mistake/3-sequential-awaits")
async def mistake_sequential():
    """
    WRONG: Awaiting coroutines one after another is sequential.
    Total time = 1s + 2s + 1.5s = 4.5s

    Each `await` waits for the previous one to finish before starting the next.
    """
    a = await _fetch_slow("A", 1)
    b = await _fetch_slow("B", 2)
    c = await _fetch_slow("C", 1.5)
    return {"results": [a, b, c]}


@app.get("/fix/3-concurrent-gather")
async def fix_concurrent():
    """
    FIX: Use gather() to run all three concurrently.
    Total time = max(1s, 2s, 1.5s) = 2s
    """
    a, b, c = await asyncio.gather(
        _fetch_slow("A", 1),
        _fetch_slow("B", 2),
        _fetch_slow("C", 1.5),
    )
    return {"results": [a, b, c]}


# ─── Mistake 4: CPU-bound work on the event loop ─────────────────────────────

def _cpu_work(n: int) -> int:
    """Intentionally slow CPU computation."""
    total = 0
    for i in range(n):
        total += i * i
    return total


@app.get("/mistake/4-cpu-on-loop")
async def mistake_cpu_on_loop():
    """
    WRONG: CPU-heavy computation directly in async def starves the event loop.
    No other requests can be served until this finishes.
    """
    result = _cpu_work(5_000_000)  # ← BLOCKS event loop
    return {"result": result}


@app.get("/fix/4-cpu-in-process")
async def fix_cpu_in_process():
    """
    FIX: Offload CPU work to a ProcessPoolExecutor.
    The event loop stays free to serve other requests.
    Note: threads don't help here because of the GIL.
    """
    loop = asyncio.get_event_loop()
    with ProcessPoolExecutor() as pool:
        result = await loop.run_in_executor(pool, _cpu_work, 5_000_000)
    return {"result": result}


# ─── Mistake 5: create_task in a plain def route ─────────────────────────────

@app.get("/mistake/5-create-task-in-def")
def mistake_create_task_in_def():
    """
    WRONG: asyncio.create_task() requires a running event loop.
    Plain `def` routes run in a threadpool — there's no event loop in that thread.
    This raises RuntimeError: no running event loop.
    """
    try:
        asyncio.create_task(log_something("test"))  # ← RuntimeError
        return {"status": "won't reach this"}
    except RuntimeError as e:
        return {"error": str(e)}


@app.get("/fix/5a-use-async-def")
async def fix_use_async_def():
    """
    FIX option A: Use async def — then create_task works because
    the route runs directly on the event loop.
    """
    asyncio.create_task(log_something("test"))
    return {"status": "logged in background"}


@app.get("/fix/5b-use-background-tasks")
def fix_use_background_tasks(bg: BackgroundTasks):
    """
    FIX option B: Use BackgroundTasks — works in both def and async def.
    The task runs after the response is sent.
    """
    bg.add_task(sync_log, "test")
    return {"status": "will log after response"}


async def log_something(msg: str):
    await asyncio.sleep(0.1)
    print(f"  [log] {msg}")


def sync_log(msg: str):
    print(f"  [log] {msg}")


# ─── Mistake 6: Not handling gather() exceptions ─────────────────────────────

async def _might_fail(label: str, should_fail: bool = False) -> str:
    await asyncio.sleep(0.5)
    if should_fail:
        raise ValueError(f"{label} failed!")
    return f"{label}: ok"


@app.get("/mistake/6-gather-no-error-handling")
async def mistake_gather_no_errors():
    """
    WRONG: gather() without return_exceptions=True raises on the FIRST error
    and orphans the remaining tasks. The other tasks keep running but their
    results are lost — and any exceptions they raise go unhandled.
    """
    try:
        results = await asyncio.gather(
            _might_fail("A"),
            _might_fail("B", should_fail=True),  # ← raises
            _might_fail("C"),                      # ← still runs, result lost
        )
        return {"results": results}
    except ValueError as e:
        return {"error": str(e), "note": "C's result was lost"}


@app.get("/fix/6-gather-with-error-handling")
async def fix_gather_with_errors():
    """
    FIX: Use return_exceptions=True to collect errors as values.
    All tasks run to completion; you inspect results individually.
    """
    results = await asyncio.gather(
        _might_fail("A"),
        _might_fail("B", should_fail=True),
        _might_fail("C"),
        return_exceptions=True,
    )
    return {
        "results": [
            str(r) if isinstance(r, Exception) else r
            for r in results
        ]
    }


# ─── Quick Reference ─────────────────────────────────────────────────────────
#
# | #  | Mistake                              | Fix                              |
# |----|--------------------------------------|----------------------------------|
# | 1  | time.sleep in async def              | asyncio.sleep                    |
# | 2  | requests.get in async def            | httpx.AsyncClient                |
# | 3  | Sequential await, await, await       | asyncio.gather or create_task    |
# | 4  | CPU work directly in async def       | ProcessPoolExecutor              |
# | 5  | create_task in plain def route       | async def or BackgroundTasks     |
# | 6  | gather without return_exceptions     | return_exceptions=True           |


if __name__ == "__main__":
    print("=== Common Async Mistakes Demo ===")
    print("Visit the /mistake/ and /fix/ routes to compare behavior.\n")
    uvicorn.run(app, host="0.0.0.0", port=8000)
