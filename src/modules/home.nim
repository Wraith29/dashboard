import solstice
import templater

proc index*(r: Request; a: RequestArgs): Response =
  let vars = newVarTable(("pageTitle", newVariable("My Personal Dashboard")))
  let templ = loadTemplate(staticRead "../templates/home.html", vars)

  return newResponse(Http200, templ)
