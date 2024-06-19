from marshmallow import Schema, fields

class RecipeSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    making_time = fields.Str(required=True)
    serves = fields.Str(required=True)
    ingredients = fields.Str(required=True)
    cost = fields.Int(required=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

class RecipeListItemSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    making_time = fields.Str(required=True)
    serves = fields.Str(required=True)
    ingredients = fields.Str(required=True)
    cost = fields.Int(required=True)

class RecipeUpdateSchema(Schema):
    title = fields.Str()
    making_time = fields.Str()
    serves = fields.Str()
    ingredients = fields.Str()
    cost = fields.Int()

class RecipeResponseSchema(Schema):
    message = fields.Str()
    recipe = fields.List(fields.Nested(RecipeSchema))

class RecipeListResponseSchema(Schema):
    recipes = fields.List(fields.Nested(RecipeListItemSchema))

class RecipePostResponseSchema(Schema):
    message = fields.Str()
    recipe = fields.List(fields.Nested(RecipeSchema))
