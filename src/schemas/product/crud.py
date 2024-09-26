# Standard Library
from typing import List, Optional
from datetime import datetime

# Third Party Library
from pydantic import BaseModel, Field

# Application Library
from src.models.products import OrderStatus


class ProductCreate(BaseModel):
	name: str
	description: Optional[str] = Field(None)
	price: float = Field(..., gt=0)
	stock_quantity: int = Field(..., ge=0)


class ProductUpdate(BaseModel):
	name: Optional[str] = Field(None)
	description: Optional[str] = Field(None)
	price: Optional[float] = Field(None, gt=0)
	stock_quantity: Optional[int] = Field(None, ge=0)


class ProductResponse(BaseModel):
	id: int
	name: str
	description: Optional[str]
	price: float
	stock_quantity: int

	class Config:
		orm_mode = True


class OrderItemCreate(BaseModel):
	product_id: int = Field(...)
	quantity: int = Field(..., ge=1)


class OrderItemUpdate(BaseModel):
	product_id: Optional[int] = Field(None)
	quantity: Optional[int] = Field(None, ge=1)


class OrderItemResponse(BaseModel):
	id: int
	product_id: int
	quantity: int


class OrderCreate(BaseModel):
	status: OrderStatus
	items: List[OrderItemCreate] = Field(...)


class OrderUpdate(BaseModel):
	status: Optional[OrderStatus] = Field(None)
	items: Optional[List[OrderItemUpdate]] = Field(None)


class OrderResponse(BaseModel):
	id: int
	created_at: datetime
	status: OrderStatus
	items: List[OrderItemResponse] = Field(...)

	class Config:
		orm_mode = True
