"""
database_async_session.py
=========================
SQLAlchemy async patterns for FastAPI.

Covers:
- Async engine and session setup
- AsyncSession as a FastAPI dependency
- Basic CRUD with async queries
- Relationship loading strategies (selectinload, joinedload)
- Transactions and error handling

Requires: sqlalchemy[asyncio], aiosqlite (for SQLite) or asyncpg (for Postgres)
"""

import asyncio

from sqlalchemy import ForeignKey, String, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, selectinload

from fastapi import Depends, FastAPI, HTTPException

app = FastAPI()


# ─── 1. Engine & Session Setup ────────────────────────────────────────────────

# Use an async driver — aiosqlite for dev, asyncpg for production Postgres
ASYNC_DATABASE_URL = "sqlite+aiosqlite:///./demo.db"

engine = create_async_engine(
    ASYNC_DATABASE_URL,
    echo=True,  # SQL logging — turn off in production
)

# async_sessionmaker replaces sessionmaker for async usage
async_session = async_sessionmaker(engine, expire_on_commit=False)


# ─── 2. Models ────────────────────────────────────────────────────────────────

class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(200), unique=True)

    # Relationship — loaded lazily by default (requires selectinload in async)
    posts: Mapped[list["Post"]] = relationship(back_populates="author")


class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    author: Mapped["User"] = relationship(back_populates="posts")


# ─── 3. Dependency — yields an AsyncSession per request ───────────────────────

async def get_db() -> AsyncSession:
    """
    FastAPI dependency that provides an AsyncSession.
    The session is automatically closed when the request finishes.
    """
    async with async_session() as session:
        yield session


# ─── 4. Routes — Basic CRUD ──────────────────────────────────────────────────

@app.on_event("startup")
async def on_startup():
    """Create tables on startup (use Alembic in real projects)."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.post("/users/")
async def create_user(name: str, email: str, db: AsyncSession = Depends(get_db)):
    """
    Insert a new user. The session is committed explicitly.
    """
    user = User(name=name, email=email)
    db.add(user)
    await db.commit()
    await db.refresh(user)  # reload to get the generated id
    return {"id": user.id, "name": user.name, "email": user.email}


@app.get("/users/{user_id}")
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    """
    Fetch a single user by ID.
    scalar_one_or_none() returns the object or None (not a Row).
    """
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"id": user.id, "name": user.name, "email": user.email}


# ─── 5. Relationship Loading ─────────────────────────────────────────────────

@app.get("/users/{user_id}/with-posts")
async def get_user_with_posts(user_id: int, db: AsyncSession = Depends(get_db)):
    """
    IMPORTANT: Lazy loading doesn't work in async SQLAlchemy.
    You MUST use an eager loading strategy.

    Options:
      selectinload — separate SELECT for related rows (good default)
      joinedload   — single JOIN query (good for one-to-one)
    """
    result = await db.execute(
        select(User)
        .where(User.id == user_id)
        .options(selectinload(User.posts))  # ← eager load posts
    )
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "id": user.id,
        "name": user.name,
        "posts": [{"id": p.id, "title": p.title} for p in user.posts],
    }


# ─── 6. Transactions ─────────────────────────────────────────────────────────

@app.post("/users/{user_id}/posts")
async def create_post_for_user(
    user_id: int, title: str, db: AsyncSession = Depends(get_db)
):
    """
    Transactional write — if anything fails, the session rolls back
    automatically when it exits the `async with` block without commit.
    """
    # Verify user exists
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    post = Post(title=title, author_id=user_id)
    db.add(post)
    await db.commit()
    await db.refresh(post)
    return {"id": post.id, "title": post.title, "author_id": post.author_id}


# ─── 7. Common Mistake: Lazy Load in Async ───────────────────────────────────

# BAD — this will raise MissingGreenlet error at runtime:
#
#   result = await db.execute(select(User).where(User.id == 1))
#   user = result.scalar_one()
#   print(user.posts)  # ← BOOM: lazy load triggers sync IO
#
# FIX — use selectinload (see route above) or access within run_sync:
#
#   async with engine.begin() as conn:
#       await conn.run_sync(lambda sync_conn: ...)


# ─── Standalone demo ─────────────────────────────────────────────────────────

async def _demo():
    """Run without FastAPI to see the queries in action."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session() as session:
        # Create
        user = User(name="Alice", email="alice@example.com")
        session.add(user)
        await session.commit()
        await session.refresh(user)
        print(f"Created user: {user.id} — {user.name}")

        # Read with eager loading
        result = await session.execute(
            select(User)
            .where(User.id == user.id)
            .options(selectinload(User.posts))
        )
        loaded_user = result.scalar_one()
        print(f"Loaded user: {loaded_user.name}, posts: {loaded_user.posts}")

    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(_demo())
