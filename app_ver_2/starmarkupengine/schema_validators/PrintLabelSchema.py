from marshmallow import Schema, fields, validate
from app_ver_2.starmarkupengine.value_validators.ValueValidators import either_true_or_false, is_non_zero_positive_float, must_not_be_blank, valid_align_values, valid_bar_codes


class PrintLabelSchema(Schema):
    # type = fields.String(validate = must_not_be_blank) 
    barcode_type = fields.String(required=True, validate=valid_bar_codes)
    # barcode_data = fields.String(required=True, validate=must_not_be_blank)
    hri = fields.Boolean(validate=either_true_or_false)
    sku = fields.String(required=True, validate=must_not_be_blank)
    upc = fields.String(validate=validate.Length(max=12, error="Max 12 chars allowed for UPC"))
    mpn = fields.String(validate=validate.Length(max=25, error="Max 50 chars allowed for MPN"))
    product_name = fields.String(required=True, validate=must_not_be_blank)
    currency_symbol = fields.String(required=True, validate=validate.Length(
        equal=1, 
        error="Field must be exactly one character long.e.g. $"))
    amount = fields.String(required=True, validate=is_non_zero_positive_float)
    qty_desc = fields.String(required=True, validate=must_not_be_blank)
    # copies = fields.Integer(validate=is_non_zero_positive_integer)
    