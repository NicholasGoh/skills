# FastAPI Async Skill

Reference for async patterns in FastAPI. Use this to answer questions about
concurrency, blocking, background work, and database sessions.

---

## Core Mental Model

The event loop is a single thread. It juggles tasks by switching between them
at **await points**. If something blocks (no yield), everything freezes.

```
Event loop tick:
  → run task A until it hits `await`
  → switch to task B until it hits `await`
  → switch back to A (or whoever is ready)
  → repeat
```

Two distinct workload types — they need different solutions:

| Type       | Examples                          | Solution               |
|------------|-----------------------------------|------------------------|
| IO-bound   | HTTP calls, DB queries, file I/O  | `async/await`, threads |
| CPU-bound  | Image processing, ML inference    | `ProcessPoolExecutor`  |

---

## FastAPI Route Decision Tree

```
Is your route handler doing IO (DB, HTTP, file)?
├── YES: async def + await async library
│         └── No async library available? → asyncio.to_thread()
└── NO (pure compute or sync-only libs):
          ├── Short work → def (FastAPI auto-runs in threadpool)
          └── Long CPU work → def + ProcessPoolExecutor inside
```

**Key rule**: `def` routes in FastAPI are automatically offloaded to a
threadpool. You don't need `async def` for everything — only when you're
actually awaiting something.

---

## Rules

### Rule 1 — Never block the event loop
Blocking calls inside `async def` freeze ALL requests, not just the current one.

```python
# BAD — blocks the entire event loop
async def get_item():
    time.sleep(2)          # freezes everything
    requests.get(url)      # same problem

# GOOD — yields control at await points
async def get_item():
    await asyncio.sleep(2)
    async with httpx.AsyncClient() as client:
        await client.get(url)
```

### Rule 2 — create_task for true concurrency
Awaiting coroutines directly is sequential. Schedule them first.

```python
# BAD — sequential, 3s total
async def handler():
    await fetch_data(1)   # waits 1s, then...
    await fetch_data(2)   # waits 2s

# GOOD — concurrent, 2s total (longest task wins)
async def handler():
    task1 = asyncio.create_task(fetch_data(1))
    task2 = asyncio.create_task(fetch_data(2))
    await task1
    await task2
```

### Rule 3 — await order ≠ execution order
`create_task` schedules immediately (FIFO). `await` only means "don't proceed
past this line until done" — it doesn't control when the task starts.

```python
task1 = asyncio.create_task(fetch_data(1))  # scheduled now
task2 = asyncio.create_task(fetch_data(2))  # scheduled now

await task2  # task1 already running in background
await task1  # both still finish in ~2s total
```

### Rule 4 — Use the right tool for sync code
```python
# Sync IO-bound (legacy libs, blocking file ops)
result = await asyncio.to_thread(blocking_io_function, arg1, arg2)

# CPU-bound (image processing, heavy computation)
loop = asyncio.get_event_loop()
with ProcessPoolExecutor() as pool:
    result = await loop.run_in_executor(pool, cpu_heavy_function, data)
```

### Rule 5 — gather() vs TaskGroup
```python
# gather() — independent tasks, partial failure OK
results = await asyncio.gather(task1(), task2(), return_exceptions=True)
# return_exceptions=True: collects errors as values, all tasks run to completion
# return_exceptions=False (default): raises on first error, orphans remaining tasks

# TaskGroup — all-or-nothing semantics
async with asyncio.TaskGroup() as tg:
    t1 = tg.create_task(task1())
    t2 = tg.create_task(task2())
# if any task fails → all cancelled → ExceptionGroup raised
```

---

## FastAPI-Specific Patterns

### Async DB Session (SQLAlchemy)
```python
# Dependency
async def get_db():
    async with AsyncSession(engine) as session:
        yield session

# Route
@app.get("/users/{id}")
async def get_user(id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.id == id))
    return result.scalar_one_or_none()
```

### Background Tasks
```python
# FastAPI BackgroundTasks — fire and forget, runs after response
@app.post("/items/")
async def create_item(bg: BackgroundTasks):
    bg.add_task(send_email, "user@example.com")  # runs after response sent
    return {"status": "queued"}

# asyncio.create_task — runs NOW on event loop (not after response)
@app.get("/items/")
async def get_items():
    asyncio.create_task(log_access())  # starts immediately, concurrent
    return await fetch_items()
```

### Parallel IO in a Route
```python
@app.get("/dashboard")
async def dashboard():
    user_task = asyncio.create_task(fetch_user())
    posts_task = asyncio.create_task(fetch_posts())
    stats_task = asyncio.create_task(fetch_stats())

    # Or with gather:
    user, posts, stats = await asyncio.gather(
        fetch_user(), fetch_posts(), fetch_stats()
    )
    return {"user": user, "posts": posts, "stats": stats}
```

---

## Performance Reference

From real-world image download + process benchmark:

| Approach                    | IO (download) | CPU (process) | Total |
|-----------------------------|---------------|---------------|-------|
| Fully synchronous           | 13s           | 10.5s         | ~23s  |
| Threads for both            | 2s            | 10.6s         | ~12s  |
| HTTPX async + ProcessPool   | 1.6s          | 3.25s         | ~5s   |

Key insight: **threads don't help CPU-bound work** (Python GIL). Use processes.

---

## Library Reference

| Task                  | Sync (avoid in async def) | Async alternative         |
|-----------------------|---------------------------|---------------------------|
| HTTP requests         | `requests`                | `httpx`, `aiohttp`        |
| Database (SQLAlchemy) | `Session`                 | `AsyncSession`            |
| File I/O              | `open()`                  | `aiofiles`                |
| Sleep/delay           | `time.sleep()`            | `asyncio.sleep()`         |
| Redis                 | `redis-py` (sync)         | `redis.asyncio`           |
| Any sync lib          | —                         | `asyncio.to_thread()`     |

---

## See Also
- `examples/route_sync_vs_async.py` — when to use def vs async def
- `examples/database_async_session.py` — SQLAlchemy async patterns
- `examples/run_in_executor.py` — CPU-bound and legacy sync code
- `examples/background_tasks.py` — BackgroundTasks vs create_task vs gather
- `examples/common_mistakes.py` — anti-patterns with explanations
- `cheatsheet.md` — quick situation → solution lookup
