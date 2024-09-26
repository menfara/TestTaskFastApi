# Standard Library
from typing import (
	Any,
	List
)

# Third Party Library
from fastapi import (
	APIRouter,
	HTTPException,
	Query
)

# Application Library
from src.crud.product import (
	product_crud,
	order_crud,
)
from src.errors import InsufficientStockError
from src.models.products import (
	Product,
	Order,
	OrderStatus
)
from src.schemas.product.crud import (
	ProductCreate,
	ProductUpdate,
	ProductResponse,
	OrderCreate,
	OrderUpdate,
	OrderResponse,
)


def check_not_empty(
	result: Any,
	detail: str = 'Resource not found'
) -> Any:
	if not result:
		raise HTTPException(
			status_code=404,
			detail=detail
		)
	return result


router = APIRouter()


@router.get(
	path='/products/',
	response_model=List[ProductResponse]
)
async def list_products(
	limit: int = Query(default=50, le=100),
	offset: int = Query(0),
	order_by: str = Query('name')
) -> List[ProductResponse]:

	order_by_column = getattr(Product, order_by, None)

	if not order_by_column:
		raise HTTPException(
			status_code=400,
			detail='Invalid order_by column'
		)

	products = await product_crud.list(
		model=Product,
		limit=limit,
		offset=offset,
		order_by=(order_by_column,)
	)

	return check_not_empty(
		result=products.all(),
		detail='Empty List'
	)


@router.post(
	path='/products/',
	response_model=ProductResponse
)
async def create_product(
	product: ProductCreate
) -> ProductResponse:
	new_product = await product_crud.create(
		model=Product,
		**product.dict()
	)
	return check_not_empty(
		result=new_product,
		detail='Product creation failed'
	)


@router.get(
	path='/products/{product_id}',
	response_model=ProductResponse
)
async def read_product(
	product_id: int
) -> ProductResponse:

	product = await product_crud.get(
		model=Product,
		conditions=(Product.id == product_id,)
	)

	return check_not_empty(
		result=product,
		detail='Product not found'
	)


@router.put(
	path='/products/{product_id}',
	response_model=ProductResponse
)
async def update_product(
	product_id: int,
	product_update: ProductUpdate
) -> ProductResponse:

	updated_product = await product_crud.update(
		model=Product,
		condition=Product.id == product_id,
		**product_update.dict(exclude_unset=True)
	)

	return check_not_empty(
		result=updated_product,
		detail='Product not found'
	)


@router.delete(
	path='/products/{product_id}',
	response_model=ProductResponse
)
async def delete_product(
	product_id: int
) -> ProductResponse:

	product = await product_crud.get(
		model=Product,
		conditions=(Product.id == product_id,)
	)

	check_not_empty(
		result=product,
		detail='Product not found'
	)

	await product_crud.delete(
		model=Product,
		condition=Product.id == product_id
	)

	return product


@router.get('/orders/', response_model=List[OrderResponse])
async def list_orders(
	limit: int = Query(default=50, le=100),
	offset: int = Query(0),
	order_by: str = Query('created_at')
) -> List[OrderResponse]:

	order_by_column = getattr(Order, order_by, None)
	if not order_by_column:
		raise HTTPException(
			status_code=400,
			detail='Invalid order_by column'
		)

	order_responses = await order_crud.list_orders(
		limit=limit,
		offset=offset,
		order_by=order_by
	)

	return check_not_empty(
		result=order_responses,
		detail='Empty List'
	)


@router.post(
	path='/orders/',
	response_model=OrderResponse
)
async def create_order(
	order: OrderCreate
) -> OrderResponse:
	try:
		new_order = await order_crud.create_order(order=order)
	except InsufficientStockError as e:
		raise HTTPException(
			status_code=400,
			detail=e.msg
		)

	return check_not_empty(
		result=new_order,
		detail='Order creation failed'
	)


@router.get(
	path='/orders/{order_id}',
	response_model=OrderResponse
)
async def read_order(
	order_id: int
) -> OrderResponse:

	order_response = await order_crud.read_order(order_id=order_id)

	return check_not_empty(
		result=order_response,
		detail='Order not found'
	)


@router.put(
	path='/orders/{order_id}',
	response_model=OrderResponse
)
async def update_order(
	order_id: int,
	order_update: OrderUpdate
) -> OrderResponse:

	updated_order_response = await order_crud.update_order(
		order_id=order_id,
		order_update=order_update
	)

	return check_not_empty(
		result=updated_order_response,
		detail='Order not found'
	)


@router.patch(
	path='/orders/{order_id}/status',
	response_model=OrderResponse
)
async def update_order_status(
	order_id: int,
	new_status: OrderStatus

) -> OrderResponse:
	updated_order_response = await order_crud.update_order_status(
		order_id=order_id,
		new_status=new_status
	)

	return check_not_empty(
		result=updated_order_response,
		detail='Order not found'
	)


@router.delete(
	path='/orders/{order_id}',
	response_model=OrderResponse
)
async def delete_order(
	order_id: int
) -> OrderResponse:
	order_response = await order_crud.delete_order(order_id=order_id)

	return check_not_empty(
		result=order_response,
		detail='Order not found'
	)
