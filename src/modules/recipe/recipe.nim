import src/db

type Recipe* = ref object

proc initTable*(): void =
  let conn = getConn()