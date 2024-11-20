from marshmallow import Schema, fields, ValidationError, validate

class BookCreateSchema(Schema):
    id = fields.Int(required=True)
    title = fields.Str(required=True, validate=validate.Length(min=1))
    author = fields.Int(required=True, validate=validate.Range(min=0, max=40))
    pages = fields.Int(required=True, validate=validate.Range(min=30, max=1500))
    
class BookUpdateSchema(Schema):
    title = fields.Str(validate=validate.Length(min=1))
    author = fields.Int(validate=validate.Range(min=0, max=40))
    pages = fields.Int(validate=validate.Range(min=30, max=1500))