from marshmallow import Schema, fields

from app_ver_2.starmarkupengine.value_validators.ValueValidators import must_not_be_blank, valid_align_values, valid_line_modes

class LineSchema(Schema):
    type = fields.String(validate = must_not_be_blank)
    mode = fields.String(required = True, validate = valid_line_modes)