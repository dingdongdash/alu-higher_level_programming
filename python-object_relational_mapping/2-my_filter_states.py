#!/usr/bin/python3
"""Displays the states whose name matches the argument given by the user."""
import MySQLdb
import sys

if __name__ == "__main__":
    db = MySQLdb.connect(host="localhost", port=3306, user=sys.argv[1],
                         passwd=sys.argv[2], db=sys.argv[3])
    cur = db.cursor()
    query = ("SELECT * FROM states WHERE name = BINARY '{}' "
             "ORDER BY states.id ASC")
    cur.execute(query.format(sys.argv[4]))
    for row in cur.fetchall():
        print(row)
    cur.close()
    db.close()
