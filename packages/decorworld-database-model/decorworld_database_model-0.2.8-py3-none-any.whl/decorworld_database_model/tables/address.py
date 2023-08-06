from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey
from marshmallow import fields
from marshmallow import Schema

from .base import Base


class Address(Base):
    __tablename__ = 'addresses'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    user_id = Column(ForeignKey('users.id'), nullable=False)
    zip_code = Column(String(4), nullable=False)
    city = Column(String(25), nullable=False)
    address = Column(String(25), nullable=False)
    description = Column(String(50), nullable=True)


class AddressSchema(Schema):

    model_class = Address

    id = fields.Integer()
    user_id = fields.Integer(load_only=True)
    zip_code = fields.String()
    city = fields.String()
    address = fields.String()
    description = fields.String()
