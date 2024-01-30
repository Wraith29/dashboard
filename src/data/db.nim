import std/[options]
import db_connector/[db_sqlite]

var conn: Option[DbConn] = none(DbConn)

proc initDb*(): void {.raises: [DbError].} =
  if conn.isNone():
    conn = some(open("dashboard.db", "", "", ""))

when defined(createDb):
  import std/[os, strutils, strformat, sugar]

  initDb()
  let initScripts = collect:
    for child in os.walkDir("src/data/sql"):
      if child.path.endsWith(".sql"):
        child.path

  for file in initScripts:
    let script = readFile(file)
    echo fmt"Executing Script: {file}"
    conn.get().exec(sql script)

proc getConn*(): Option[DbConn] {.raises: [DbError].} =
  if conn.isNone(): initDb()

  return conn
