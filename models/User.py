from marshmallow import Schema, fields, ValidationError, validate, validates

class UserSchema(Schema):
    username = fields.Str(validate=validate.Length(min=1))
    password = fields.Str( validate=validate.Regexp(
        r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\W).{8,}$',
        error="Password must have at least one lower and upper case letter and one character")
    )
    email = fields.Email()
    age = fields.Integer(validate=validate.Range(min=18, max=90))
