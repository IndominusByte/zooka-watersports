import re
from marshmallow import Schema, fields, validate, validates, validates_schema, ValidationError
from services.models.VoucherModel import Voucher
from services.models.ActivityModel import Activity

class VoucherSchema(Schema):
    id = fields.Int(dump_only=True)
    # image
    # thumbnail
    title = fields.Str(required=True,validate=validate.Length(min=5,max=100))
    code = fields.Str(required=True,validate=validate.Length(min=5,max=100))
    valid_start = fields.Str(required=True,validate=validate.Length(min=3,max=100))
    valid_end = fields.Str(required=True,validate=validate.Length(min=3,max=100))
    description = fields.Str(required=True,validate=validate.Length(min=5))
    discount = fields.Int(required=True,validate=validate.Range(min=1,error="Value must be greater than 0"))
    type_voucher = fields.Str(required=True,validate=validate.Length(min=3,max=100))
    minimum = fields.Int(required=True,validate=validate.Range(min=1,error="Value must be greater than 0"))
    terms = fields.Str(required=True,validate=validate.Length(min=5))
    # seen
    # created_at
    # updated_at
    activity_id = fields.Int(validate=validate.Range(min=1,error="Value must be greater than 0"))

    @validates('title')
    def validate_title(self,value):
        if Voucher.query.filter_by(title=value).first():
            raise ValidationError('The title has already been taken.')

    @validates('code')
    def validate_code(self,value):
        if Voucher.query.filter_by(code=value).first():
            raise ValidationError('The code has already been taken.')

    @validates('valid_start')
    def validate_valid_start(self,value):
        if not re.match(r"^\d{4}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])$",value):
            raise ValidationError('Invalid date format.')

    @validates('valid_end')
    def validate_valid_end(self,value):
        if not re.match(r"^\d{4}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])$",value):
            raise ValidationError('Invalid date format.')

    @validates('discount')
    def validate_discount(self,value):
        if value < 10000:
            raise ValidationError('Discount cannot less than IDR. 10.000')

    @validates('type_voucher')
    def validate_type_voucher(self,value):
        if value not in ['Person','Transaction']:
            raise ValidationError('Invalid voucher type.')

    @validates('activity_id')
    def validate_activity_id(self,value):
        if not Activity.query.get(value):
            raise ValidationError('Activity not found')

    @validates_schema
    def validate_minimum(self,data,**kwargs):
        if data['type_voucher'] == 'Person':
            if data['minimum'] > 100:
                raise ValidationError({'minimum':['Minimum cannot greater than 100']})
        if data['type_voucher'] == 'Transaction':
            if data['minimum'] < 10000:
                raise ValidationError({'minimum':['Minimum cannot less than IDR. 10.000']})
