from services.serve import db
from datetime import datetime

class Voucher(db.Model):
    __tablename__ = 'vouchers'

    id = db.Column(db.Integer,primary_key=True)
    image = db.Column(db.String(100),nullable=False)
    thumbnail = db.Column(db.String(100),nullable=False)
    title = db.Column(db.String(100),unique=True,index=True,nullable=False)
    slug = db.Column(db.Text,nullable=False)
    code = db.Column(db.String(100),unique=True,index=True,nullable=False)
    valid_start = db.Column(db.String(100),nullable=False)
    valid_end = db.Column(db.String(100),nullable=False)
    description = db.Column(db.Text,nullable=False)
    discount = db.Column(db.Integer,nullable=False)
    type_voucher = db.Column(db.String(100),nullable=False)
    minimum = db.Column(db.Integer,nullable=False)
    terms = db.Column(db.Text,nullable=False)
    seen = db.Column(db.Boolean,default=False)
    created_at = db.Column(db.DateTime,default=datetime.now)
    updated_at = db.Column(db.DateTime,default=datetime.now)

    activity_id = db.Column(db.Integer,db.ForeignKey('activities.id'),nullable=True)

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
