from marshmallow import Schema, fields

class RecipeSchema(Schema):
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
