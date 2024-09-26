class InsufficientStockError(Exception):
	def __init__(
		self,
		product_id: int,
		available_stock: int,
		requested_quantity: int
	):
		self.product_id = product_id
		self.available_stock = available_stock
		self.requested_quantity = requested_quantity
		self.msg = (
			f"Insufficient stock for product ID {product_id}. "
			f"Available: {available_stock}, "
			f"Requested: {requested_quantity}"
		)
		super().__init__(self.msg)
