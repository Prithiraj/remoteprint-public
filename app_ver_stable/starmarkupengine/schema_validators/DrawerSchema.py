from marshmallow import Schema, fields

from app_ver_stable.starmarkupengine.value_validators.ValueValidators import valid_drawer_open_values, validate_buzzers_count

class DrawerSchema(Schema):
	openAt = fields.String(required=True, validate=valid_drawer_open_values)
