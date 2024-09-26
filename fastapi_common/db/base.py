# Standard Library
from typing import Any

# Third Party Library
from sqlalchemy.ext.declarative import (
	as_declarative,
	declared_attr,
)
from sqlalchemy.orm import declarative_base

__all__ = (
	'BaseModel',
)

Base = declarative_base()


class BaseModel(Base):
	__abstract__ = True
	id: Any
	__name__: str

	@declared_attr
	def __tablename__(
		cls
	) -> str:
		return cls.__name__.lower()

	def __init__(
		self,
		*args,
		**kwargs
	):  # pragma: no cover
		super().__init__(*args, **kwargs)
