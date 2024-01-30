import std/[options, os]
import db_connector/[db_sqlite]

var conn: Option[DbConn] = none(DbConn)

proc getInitScripts(): seq[string] {.raises: [OSError].} =
  for child in os.walkDir("./sql", true):
    if child.kind != pcFile:
      continue

    result.add(child.path)

proc initDb*(): void {.raises: [DbError, IOError].} =
  if conn.isNone():
    conn = some(open("dashboard.db", "", "", ""))

  const initScripts = static getInitScripts()

  for file in initScripts:
    let script = readFile(file)
    echo "Sql Script: ", script
    conn.get().exec(sql script)

proc getConn*(): Option[DbConn] {.raises: [IOError].} =
  if conn.isNone(): initDb()

  return conn
