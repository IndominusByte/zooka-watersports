from marshmallow import Schema, fields, validate, validates, ValidationError
from services.models.CategoryModel import Category

class ActivitySchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True,validate=validate.Length(min=3,max=100))
    slug = fields.Str(dump_only=True)
    description = fields.Str(required=True,validate=validate.Length(min=3))
    duration = fields.Str(required=True,validate=validate.Length(min=3,max=100))
    discount = fields.Int(validate=validate.Range(min=1,error="Value must be greater than 0"))
    price = fields.Int(required=True,validate=validate.Range(min=1,error="Value must be greater than 0"))
    min_person = fields.Int(required=True,validate=validate.Range(min=1,max=100))
    include = fields.Str(required=True,validate=validate.Length(min=3))
    pickup = fields.Str(required=True,validate=validate.Length(min=3,max=100))
    information = fields.Str(required=True,validate=validate.Length(min=3))
    image = fields.Str(dump_only=True)
    image2 = fields.Str(dump_only=True)
    image3 = fields.Str(dump_only=True)
    image4 = fields.Str(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    category_id = fields.Int(required=True,validate=validate.Range(min=1,error="Value must be greater than 0"))

    category = fields.Nested("CategorySchema",only=("name",))

    @validates('category_id')
    def validate_category_id(self,value):
        if not Category.query.get(value):
            raise ValidationError('Category not found')

    @validates('discount')
    def validate_discount(self,value):
        if value < 10000:
            raise ValidationError('Discount cannot less than IDR. 10.000')

    @validates('price')
    def validate_price(self,value):
        if value < 10000:
            raise ValidationError('Price cannot less than IDR. 10.000')
