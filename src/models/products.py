# Standard Library
from enum import Enum as PyEnum
from datetime import datetime

# Third Party Library
from sqlalchemy import (
	Column,
	Integer,
	String,
	Float,
	DateTime,
	Enum,
	ForeignKey
)
from sqlalchemy.orm import relationship

# Application Library
from fastapi_common.db.base import BaseModel


class OrderStatus(PyEnum):
	IN_PROGRESS = "в процессе"
	SHIPPED = "отправлен"
	DELIVERED = "доставлен"


class Product(BaseModel):
	__tablename__ = 'products'

	id = Column(
		Integer,
		primary_key=True,
		index=True
	)
	name = Column(
		String(255),
		nullable=False
	)
	description = Column(
		String(500),
		nullable=True
	)
	price = Column(
		Float,
		nullable=False
	)
	stock_quantity = Column(
		Integer,
		nullable=False
	)

	def __repr__(
		self
	):
		return f"<Product(id={self.id}, name={self.name}, price={self.price})>"


class Order(BaseModel):
	__tablename__ = 'orders'

	id = Column(
		Integer,
		primary_key=True,
		index=True
	)
	created_at = Column(
		DateTime,
		default=datetime.utcnow
	)
	status = Column(
		Enum(OrderStatus),
		default=OrderStatus.IN_PROGRESS
	)

	items = relationship(
		"OrderItem",
		back_populates="order"
	)

	def __repr__(
		self
	):
		return f"<Order(id={self.id}, status={self.status})>"


class OrderItem(BaseModel):
	__tablename__ = 'order_items'

	id = Column(
		Integer,
		primary_key=True,
		index=True
	)

	order_id = Column(
		Integer,
		ForeignKey('orders.id'),
		nullable=False
	)
	product_id = Column(
		Integer,
		ForeignKey('products.id'),
		nullable=False
	)
	quantity = Column(
		Integer,
		nullable=False
	)

	# Relationships
	order = relationship(
		"Order",
		back_populates="items"
	)
	product = relationship("Product")

	def __repr__(
		self
	):
		return f"<OrderItem(id={self.id}, order_id={self.order_id}, product_id={self.product_id}, quantity={self.quantity})>"
