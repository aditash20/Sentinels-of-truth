import sqlite3
import csv

DB_NAME = "sentinels.db"
OUTPUT_FILE = "sentinels_export.csv"


def export_to_csv():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM messages")

    rows = cursor.fetchall()
    headers = [desc[0] for desc in cursor.description]

    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        writer.writerow(headers)
        writer.writerows(rows)

    conn.close()

    print(f"Exported {len(rows)} rows to {OUTPUT_FILE}")


if __name__ == "__main__":
    export_to_csv()