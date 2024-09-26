# Standard Library
from typing import (
	List,
	Optional,
	Dict
)

# Third Party Library
from sqlalchemy import and_
from sqlalchemy.orm import selectinload

# Application Library
from fastapi_common.crud import BaseCRUD
from src.errors import InsufficientStockError
from src.models import (
	Product,
	Order,
	OrderItem
)
from src.schemas.product.crud import (
	OrderResponse,
	OrderItemResponse,
	OrderUpdate
)


class ProductCRUD(BaseCRUD):
	async def check_stock(
		self,
		product_ids: List[int]
	) -> Dict[int, int]:
		stock_check_results = await self.list(
			model=Product,
			conditions=(Product.id.in_(product_ids),),
		)
		results = {
			product.id: product.stock_quantity
			for product in stock_check_results
		}

		return results

	async def update_stock_quantity(
		self,
		product_id: int,
		new_stock_quantity: int
	) -> None:
		await self.update(
			model=Product,
			condition=(Product.id == product_id),
			stock_quantity=new_stock_quantity
		)


class OrderCRUD(BaseCRUD):

	def _format_order_response(
		self,
		order: Order
	) -> OrderResponse:
		order_items_response = [
			OrderItemResponse(
				id=item.id,
				product_id=item.product_id,
				quantity=item.quantity
			)
			for item in order.items
		]

		return OrderResponse(
			id=order.id,
			created_at=order.created_at,
			status=order.status,
			items=order_items_response
		)

	async def delete_order(
		self,
		order_id: int
	) -> Optional[OrderResponse]:
		order = await self.get(
			model=Order,
			conditions=(Order.id == order_id,),
			options=(selectinload(Order.items),)
		)
		if not order:
			return None

		await self.delete(
			model=OrderItem,
			condition=OrderItem.order_id == order_id
		)
		await self.delete(
			model=Order,
			condition=Order.id == order_id
		)

		return self._format_order_response(order)

	async def read_order(
		self,
		order_id: int
	) -> Optional[OrderResponse]:
		order = await self.get(
			model=Order,
			conditions=(Order.id == order_id,),
			options=(selectinload(Order.items),)
		)
		if not order:
			return None

		return self._format_order_response(order)

	async def update_order(
		self,
		order_id: int,
		order_update: OrderUpdate
	) -> Optional[OrderResponse]:
		current_order = await self.get(
			model=Order,
			conditions=(Order.id == order_id,)
		)

		if not current_order or not order_update.items:
			return None

		for item in order_update.items:
			await self._update_or_create_order_item(
				order_id,
				item
			)

		updated_order = await self.get(
			model=Order,
			conditions=(Order.id == order_id,),
			options=(selectinload(Order.items),)
		)

		return self._format_order_response(updated_order)

	async def _update_or_create_order_item(
		self,
		order_id: int,
		item
	) -> None:
		condition = and_(
			OrderItem.order_id == order_id,
			OrderItem.product_id == item.product_id
		)

		existing_item = await self.get(
			model=OrderItem,
			conditions=condition
		)

		if existing_item:
			await self.update(
				model=OrderItem,
				condition=condition,
				quantity=item.quantity
			)
		else:
			await self.create(
				model=OrderItem,
				order_id=order_id,
				product_id=item.product_id,
				quantity=item.quantity
			)

	async def list_orders(
		self,
		limit: int,
		offset: int,
		order_by: str
	) -> List[OrderResponse]:
		orders = await self.list(
			model=Order,
			limit=limit,
			offset=offset,
			order_by=(getattr(Order, order_by),),
			options=(selectinload(Order.items),)
		)
		orders = [
			self._format_order_response(order)
			for order in orders
		]

		return orders

	async def create_order(
		self,
		order
	) -> Optional[OrderResponse]:
		await self._check_stock_availability(order)

		new_order = await self.create(
			model=Order,
			status=order.status
		)

		await self._create_order_items(
			new_order.id,
			order.items
		)

		updated_order = await self.get(
			model=Order,
			conditions=(Order.id == new_order.id,),
			options=(selectinload(Order.items),)
		)

		return self._format_order_response(updated_order)

	async def _check_stock_availability(
		self,
		order
	) -> None:
		stock_dict = await product_crud.check_stock(
			[item.product_id for item in order.items])

		for item in order.items:
			available_stock = stock_dict.get(item.product_id, 0)
			if available_stock < item.quantity:
				raise InsufficientStockError(
					product_id=item.product_id,
					available_stock=available_stock,
					requested_quantity=item.quantity
				)

	async def _create_order_items(
		self,
		order_id: int,
		items
	) -> None:
		stock_dict = await product_crud.check_stock(
			[item.product_id for item in items])

		for item in items:
			await self.create(
				model=OrderItem,
				order_id=order_id,
				product_id=item.product_id,
				quantity=item.quantity
			)
			new_stock_quantity = stock_dict[item.product_id] - item.quantity
			await product_crud.update_stock_quantity(
				product_id=item.product_id,
				new_stock_quantity=new_stock_quantity
			)

	async def update_order_status(
		self,
		order_id: int,
		new_status: str
	) -> Optional[OrderResponse]:
		order = await self.get(
			model=Order,
			conditions=(Order.id == order_id,)
		)
		if not order:
			return None

		await self.update(
			model=Order,
			condition=(Order.id == order_id),
			status=new_status
		)

		updated_order = await self.get(
			model=Order,
			conditions=(Order.id == order_id,),
			options=(selectinload(Order.items),)
		)

		return self._format_order_response(updated_order)


product_crud = ProductCRUD()
order_crud = OrderCRUD()
