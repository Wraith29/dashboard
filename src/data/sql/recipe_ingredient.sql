CREATE TABLE IF NOT EXISTS 'RecipeIngredient' (
    [RecipeId] INTEGER NOT NULL,
    [IngredientId] INTEGER NOT NULL,
    [Measurement] TEXT NOT NULL,
    [Quantity] INTEGER NOT NULL,
    FOREIGN KEY ([RecipeId]) REFERENCES [Recipe]([Id]),
    FOREIGN KEY ([IngredientId]) REFERENCES [Ingredient]([Id])
)