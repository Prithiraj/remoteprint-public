from marshmallow import Schema, fields
from app_ver_2.starmarkupengine.value_validators.ValueValidators import either_true_or_false, must_not_be_blank, valid_align_values, valid_bar_codes


class BarCodeSchema(Schema):
    type = fields.String(validate = must_not_be_blank) 
    align = fields.String(validate = valid_align_values)
    barcode_type = fields.String(required=True, validate=valid_bar_codes)
    data = fields.String(required=True, validate=must_not_be_blank)
    hri = fields.Boolean(validate=either_true_or_false)
    