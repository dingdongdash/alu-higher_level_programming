#!/usr/bin/python3
"""Displays the states matching the user argument without SQL injection."""
import MySQLdb
import sys

if __name__ == "__main__":
    db = MySQLdb.connect(host="localhost", port=3306, user=sys.argv[1],
                         passwd=sys.argv[2], db=sys.argv[3])
    cur = db.cursor()
    cur.execute("SELECT * FROM states WHERE name = %s "
                "ORDER BY states.id ASC", (sys.argv[4],))
    for row in cur.fetchall():
        print(row)
    cur.close()
    db.close()
