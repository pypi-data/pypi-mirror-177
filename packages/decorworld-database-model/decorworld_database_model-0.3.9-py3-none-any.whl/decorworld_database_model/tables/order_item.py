from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import ForeignKey
from marshmallow import fields
from marshmallow import Schema
from marshmallow import post_load

from .base import Base


class OrderItem(Base):
    __tablename__ = 'order_items'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    order_id = Column(ForeignKey('orders.id'), nullable=False)
    product_id = Column(ForeignKey('products.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Integer, nullable=False)


class OrderItemSchema(Schema):

    model_class = OrderItem

    id = fields.Integer()
    order_id = fields.Integer(data_key='orderID')
    product_id = fields.Integer(data_key='productID')
    quantity = fields.Integer()
    price = fields.Integer()

    @post_load
    def make_address(self, data, **kwargs):
        return OrderItem(**data)
