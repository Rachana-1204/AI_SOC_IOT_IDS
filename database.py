import sqlite3

DB = "threats.db"

# =====================================================

def init_db():

    conn = sqlite3.connect(DB)

    cur = conn.cursor()

    cur.execute("""

    CREATE TABLE IF NOT EXISTS threats(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        device TEXT,

        attack TEXT,

        severity TEXT,

        confidence REAL,

        country TEXT,

        explanation TEXT,

        time TEXT

    )

    """)

    conn.commit()

    conn.close()

# =====================================================

def insert_threat(item):

    conn = sqlite3.connect(DB)

    cur = conn.cursor()

    cur.execute("""

    INSERT INTO threats(

        device,
        attack,
        severity,
        confidence,
        country,
        explanation,
        time

    )

    VALUES(?,?,?,?,?,?,?)

    """, (

        item['device'],
        item['attack'],
        item['severity'],
        item['confidence'],
        item['country'],
        item['explanation'],
        item['time']

    ))

    conn.commit()

    conn.close()

# =====================================================

def get_all_threats():

    conn = sqlite3.connect(DB)

    cur = conn.cursor()

    cur.execute(

        "SELECT * FROM threats"
    )

    data = cur.fetchall()

    conn.close()

    return data