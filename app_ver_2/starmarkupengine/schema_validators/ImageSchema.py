from marshmallow import Schema, fields

from app_ver_2.starmarkupengine.value_validators.ValueValidators import must_not_be_blank, valid_align_values

class ImageSchema(Schema):
    align = fields.String(validate=valid_align_values)
    type = fields.String(required=True, validate=must_not_be_blank)
    url = fields.String(required=True, validate=must_not_be_blank)
    width = fields.String(validate=must_not_be_blank)
    min_width= fields.String(validate=must_not_be_blank)