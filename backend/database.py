import os
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone

DB_PATH = os.path.join(os.path.dirname(__file__), "data", "app.db")


def get_db_path():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    return DB_PATH


@contextmanager
def get_db():
    conn = sqlite3.connect(get_db_path())
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def init_db():
    """初始化数据库表结构"""
    with get_db() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TEXT DEFAULT (datetime('now')),
                updated_at TEXT DEFAULT (datetime('now'))
            );

            CREATE TABLE IF NOT EXISTS video_parse_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                video_id TEXT NOT NULL,
                platform TEXT NOT NULL,
                source_url TEXT NOT NULL,
                title TEXT NOT NULL,
                thumbnail TEXT,
                uploader TEXT,
                duration INTEGER,
                duration_string TEXT,
                parsed_at TEXT NOT NULL,
                created_at TEXT DEFAULT (datetime('now')),
                updated_at TEXT DEFAULT (datetime('now')),
                FOREIGN KEY (user_id) REFERENCES users(id)
            );

            CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
            CREATE INDEX IF NOT EXISTS idx_history_user_id ON video_parse_history(user_id);
            CREATE INDEX IF NOT EXISTS idx_history_user_parsed_at ON video_parse_history(user_id, parsed_at DESC);
            CREATE UNIQUE INDEX IF NOT EXISTS idx_history_user_video ON video_parse_history(user_id, platform, video_id);
        """)


def get_user_by_email(email: str) -> dict | None:
    with get_db() as conn:
        row = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
        return dict(row) if row else None


def get_user_by_id(user_id: int) -> dict | None:
    with get_db() as conn:
        row = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
        return dict(row) if row else None


def create_user(email: str, password_hash: str) -> dict:
    with get_db() as conn:
        cursor = conn.execute(
            "INSERT INTO users (email, password_hash) VALUES (?, ?)",
            (email, password_hash),
        )
        return {"id": cursor.lastrowid, "email": email}


def check_and_increment_summary(user_id: int) -> tuple[bool, int]:
    """
    检查用户是否可以使用 AI 总结。
    项目已移除会员和额度限制，存在的用户均可无限使用。
    返回 (allowed, remaining_count)
    """
    with get_db() as conn:
        user = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
        if not user:
            return False, 0

        return True, -1


def upsert_video_history(user_id: int, source_url: str, video_data: dict) -> None:
    now = datetime.now(timezone.utc).isoformat()
    video_id = video_data.get("id") or source_url
    platform = video_data.get("platform") or "unknown"

    with get_db() as conn:
        conn.execute(
            """
            INSERT INTO video_parse_history (
                user_id, video_id, platform, source_url, title, thumbnail,
                uploader, duration, duration_string, parsed_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(user_id, platform, video_id) DO UPDATE SET
                source_url = excluded.source_url,
                title = excluded.title,
                thumbnail = excluded.thumbnail,
                uploader = excluded.uploader,
                duration = excluded.duration,
                duration_string = excluded.duration_string,
                parsed_at = excluded.parsed_at,
                updated_at = excluded.updated_at
            """,
            (
                user_id,
                video_id,
                platform,
                source_url,
                video_data.get("title", "未知标题"),
                video_data.get("thumbnail", ""),
                video_data.get("uploader", ""),
                video_data.get("duration"),
                video_data.get("duration_string", "00:00"),
                now,
                now,
            ),
        )


def count_user_video_history(user_id: int) -> int:
    with get_db() as conn:
        row = conn.execute(
            "SELECT COUNT(*) AS count FROM video_parse_history WHERE user_id = ?",
            (user_id,),
        ).fetchone()
        return int(row["count"]) if row else 0


def get_user_video_history(user_id: int, offset: int = 0, limit: int = 20) -> tuple[list[dict], int]:
    with get_db() as conn:
        rows = conn.execute(
            """
            SELECT id, video_id, platform, source_url, title, thumbnail,
                   uploader, duration, duration_string, parsed_at
            FROM video_parse_history
            WHERE user_id = ?
            ORDER BY parsed_at DESC, id DESC
            LIMIT ? OFFSET ?
            """,
            (user_id, limit, offset),
        ).fetchall()
        total_row = conn.execute(
            "SELECT COUNT(*) AS count FROM video_parse_history WHERE user_id = ?",
            (user_id,),
        ).fetchone()
        total = int(total_row["count"]) if total_row else 0
        return [dict(row) for row in rows], total
