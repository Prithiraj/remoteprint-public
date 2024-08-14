from jinja2 import pass_eval_context
from marshmallow import Schema, ValidationError, fields, validates_schema

from app_ver_2.starmarkupengine.value_validators.ValueValidators import validate_buzzers_count

class BuzzerCountSchema(Schema):
    start = fields.Integer(required=True, validate = validate_buzzers_count)
    end = fields.Integer(validate = validate_buzzers_count)
    
    @validates_schema
    def validate_requirement(self, data, **kwargs):
        if "start" in data or "end" in data:
            pass
        else:
            raise ValidationError("Either of start or end field must be there")
        # else: 
