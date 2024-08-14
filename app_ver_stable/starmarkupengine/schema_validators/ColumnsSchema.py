from marshmallow import Schema, fields

from app_ver_stable.starmarkupengine.value_validators.ValueValidators import must_not_be_blank, valid_align_values


# class ColumnLineSchema(Schema):
#     type = fields.String()

class SubColumnSchema(Schema):
    left = fields.String(required=True, validate=must_not_be_blank)
    right = fields.String(required=True, validate=must_not_be_blank)
    short = fields.String()

class ColumnSchema(Schema):
	left = fields.String(required=True, validate=must_not_be_blank)
	short = fields.String()
	right = fields.String(required=True, validate=must_not_be_blank)
	sub = fields.List(fields.Nested(SubColumnSchema, validate=must_not_be_blank))
	# line = fields.String()
 

class ColumnsSchema(Schema):
	align = fields.String(validate=valid_align_values)
	type = fields.String(validate = must_not_be_blank)
	value = fields.Dict(validate=must_not_be_blank)	
	indent = fields.String()
	columns = fields.List(fields.Nested(ColumnSchema, validate=must_not_be_blank))
    