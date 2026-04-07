# FastAPI Async Cheatsheet

Quick lookup: "I have X situation, do Y"

---

## Situation → Solution

### "I need to call an external HTTP API"
```python
# Use httpx (async). Never use requests inside async def.
async with httpx.AsyncClient() as client:
    response = await client.get("https://api.example.com/data")
```

### "I need to call multiple external APIs and wait for all"
```python
# Use gather — runs concurrently, not sequentially
user, posts = await asyncio.gather(
    fetch_user(user_id),
    fetch_posts(user_id),
)
```

### "I need to call multiple APIs but one failing shouldn't kill others"
```python
results = await asyncio.gather(
    fetch_user(id), fetch_posts(id), fetch_stats(id),
    return_exceptions=True
)
# Each result is either the value or an Exception instance
```

### "I need to call multiple APIs and ALL must succeed or rollback"
```python
async with asyncio.TaskGroup() as tg:
    t1 = tg.create_task(charge_card())
    t2 = tg.create_task(reserve_inventory())
# If either fails → both cancelled → ExceptionGroup raised
```

### "I'm using a library that doesn't have async support (e.g. legacy SDK)"
```python
# Wrap it with to_thread — runs in threadpool, non-blocking
result = await asyncio.to_thread(legacy_sdk.do_thing, arg1, arg2)
```

### "I need to do CPU-heavy work (image resize, data transform, ML)"
```python
from concurrent.futures import ProcessPoolExecutor

loop = asyncio.get_event_loop()
with ProcessPoolExecutor() as pool:
    result = await loop.run_in_executor(pool, cpu_heavy_fn, data)
# Runs in a separate process — bypasses the GIL
```

### "I want to send an email / log something after the response is returned"
```python
# FastAPI BackgroundTasks — fire and forget
@app.post("/signup")
async def signup(user: UserIn, bg: BackgroundTasks):
    await create_user(user)
    bg.add_task(send_welcome_email, user.email)  # runs after response
    return {"status": "created"}
```

### "I want something to run NOW, concurrently with the current request"
```python
# create_task schedules immediately on the event loop
asyncio.create_task(log_request(request_id))
# Does NOT wait — continues executing current route
```

### "I'm not doing any async IO — should I use async def?"
```python
# No. Use plain def — FastAPI runs it in a threadpool automatically.
@app.get("/config")
def get_config():
    return {"debug": settings.DEBUG}  # no await needed, no async needed
```

### "My route uses a sync DB driver (psycopg2, pymysql)"
```python
# Use plain def — FastAPI threadpool keeps event loop free
@app.get("/users/{id}")
def get_user(id: int, db: Session = Depends(get_db)):
    return db.query(User).filter(User.id == id).first()

# OR: wrap in to_thread if you must use async def
async def get_user(id: int):
    return await asyncio.to_thread(sync_db_query, id)
```

### "My async route is slow even though I'm using async def"
Checklist:
1. Are you awaiting coroutines sequentially instead of using `create_task`/`gather`?
2. Are you using `time.sleep` instead of `asyncio.sleep`?
3. Are you using a sync library (`requests`, `psycopg2`) inside `async def`?
4. Are you doing CPU-heavy work on the event loop instead of a process pool?

### "I need to start tasks and collect results later"
```python
# Schedule first, await later — both run concurrently
task1 = asyncio.create_task(fetch_data(1))
task2 = asyncio.create_task(fetch_data(2))

do_other_work()  # runs while tasks are in flight

result1 = await task1
result2 = await task2
```

### "Should I use gather() or create_task + await?"
```
create_task + await:
  → Fine for small numbers of tasks
  → Explicit, easy to name and reference tasks
  → Can do other work between create and await

gather():
  → Cleaner for many coroutines at once
  → Returns list of results in input order
  → return_exceptions=True for fault-tolerant fan-out
```

---

## Anti-Pattern Quick Reference

| You wrote this                         | Problem                          | Fix                              |
|----------------------------------------|----------------------------------|----------------------------------|
| `time.sleep(n)` in `async def`        | Blocks entire event loop         | `await asyncio.sleep(n)`         |
| `requests.get(url)` in `async def`    | Blocks entire event loop         | `httpx.AsyncClient().get(url)`   |
| `await coro1(); await coro2()`         | Sequential, not concurrent       | `create_task` or `gather`        |
| Sync SQLAlchemy `Session` in `async def` | Blocks event loop             | `AsyncSession` or use `def`      |
| CPU work directly in `async def`      | Starves other requests           | `run_in_executor(ProcessPool)` |
| `asyncio.create_task()` in `def` route | No event loop context            | Use `BackgroundTasks` instead   |
