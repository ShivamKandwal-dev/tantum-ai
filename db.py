import sqlite3

DB_PATH = "jobs.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            job_id TEXT PRIMARY KEY,
            status TEXT,
            video_path TEXT,
            result_url TEXT
        )
    """)
    conn.commit()
    conn.close()

def add_job(job_id, status, video_path):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO jobs VALUES (?, ?, ?, ?)",
              (job_id, status, video_path, None))
    conn.commit()
    conn.close()

def get_job(job_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM jobs WHERE job_id=?", (job_id,))
    row = c.fetchone()
    conn.close()

    if not row:
        return None
    return {
        "job_id": row[0],
        "status": row[1],
        "video_path": row[2],
        "result_url": row[3]
    }

def update_job_status(job_id, status, result_url=None):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "UPDATE jobs SET status=?, result_url=? WHERE job_id=?",
        (status, result_url, job_id)
    )
    conn.commit()
    conn.close()
