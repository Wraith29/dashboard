import solstice

proc getAllRecipes(r: Request; a: RequestArgs): Response =
  return newResponse(Http200, "Get All Recipes")

proc recipeModule*(): Module =
  result = newModule("/recipe")

  result.get("/", getAllRecipes)