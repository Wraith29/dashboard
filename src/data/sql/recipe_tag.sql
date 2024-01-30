CREATE TABLE IF NOT EXISTS 'RecipeTag' (
    [RecipeId] INTEGER NOT NULL,
    [TagId] INTEGER NOT NULL,
    FOREIGN KEY ([RecipeId]) REFERENCES [Recipe]([Id]),
    FOREIGN KEY ([TagId]) REFERENCES [Tag]([Id])
)