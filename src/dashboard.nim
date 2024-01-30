import std/[asyncdispatch]
import solstice
import src/modules/[home, recipe], data/[db]

proc main(): Future[void] {.async.} =
  initDb()

  var app = newApi(3000)

  app.get("/", home.index)
  app.register(recipeModule())

  for route in app.routes:
    echo route.route

  waitFor app.run(true)

when isMainModule:
  waitFor main()