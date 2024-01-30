# Package

version       = "0.1.0"
author        = "Isaac Naylor"
description   = "A new awesome nimble package"
license       = "MIT"
srcDir        = "src"
bin           = @["dashboard"]


# Dependencies

requires "nim >= 2.1.1"
requires "templater"
requires "https://github.com/Wraith29/solstice"
requires "db_connector"

task docs, "Docs":
  exec "nim doc --project -o:./docs ./src/dashboard.nim"

task test, "Run all Tests":
  exec "testament cat ." 
  exec "testament html"