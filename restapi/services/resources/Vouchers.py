from flask_restful import Resource, request
from flask_jwt_extended import jwt_required
from services.schemas.vouchers.VoucherSchema import VoucherSchema
from services.schemas.vouchers.AddImageVoucherSchema import AddImageVoucherSchema
from services.middleware.Admin import admin_required
from services.models.VoucherModel import Voucher
from services.libs.MagicImage import MagicImage

_voucher_schema = VoucherSchema()

class CreateVoucher(Resource):
    @jwt_required
    @admin_required
    def post(self):
        _image_schema = AddImageVoucherSchema()
        file = _image_schema.load(request.files)
        data = _voucher_schema.load(request.form)
        # save image voucher
        magic_image = MagicImage(file=file['image'],width=2000,height=300,path_upload='vouchers/',square=False)
        magic_image.save_image()
        # crop image voucher to make thumbnail
        magic_image = MagicImage(file=file['image'],width=650,height=300,path_upload='vouchers/thumbnail/',square=False)
        magic_image.save_image()

        print(file)
        print(data)
