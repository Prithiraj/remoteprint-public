from marshmallow import Schema, fields

from app_ver_1.starmarkupengine.value_validators.ValueValidators import must_not_be_blank, valid_align_values

class ContentSchema(Schema):
	align = fields.String(validate=valid_align_values)
	type = fields.String(validate=must_not_be_blank)
	content = fields.List(fields.String, required=True, validate=must_not_be_blank)