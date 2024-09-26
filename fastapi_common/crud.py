# Standard Library
from functools import reduce
from typing import List

# Third Party Library
from .db import create_session
from sqlalchemy import (
    delete,
    select,
    update,
)


class BaseCRUD:
    async def list(
            self,
            model,
            conditions: tuple = None,
            joins: List[tuple] = None,
            order_by: tuple = None,
            limit: int = None,
            offset: int = None,
            options: tuple = None,
            session=None
    ):
        query = select(model)
        if joins:
            query = reduce(lambda x, y: x.join(*y), joins, query)
        if conditions is not None:
            query = reduce(
                lambda x, y: x.where(y) if y is not None else x,
                conditions,
                query
            )
        if order_by:
            query = query.order_by(*order_by)
        if limit:
            query = query.limit(limit)
        if offset:
            query = query.offset(offset)
        if options:
            query = query.options(*options)
        async with create_session(session) as session:
            return (await session.execute(query)).scalars().unique()

    async def get(
            self,
            model,
            conditions: tuple,
            joins: List[tuple] = None,
            order_by: tuple = None,
            offset: int = None,
            options: tuple = None,
            session=None
    ):
        return (
            await self.list(
                model=model,
                conditions=conditions,
                joins=joins,
                order_by=order_by,
                offset=offset,
                options=options,
                session=session
            )
        ).first()

    async def create(
            self,
            model,
            session=None,
            commit=True,
            **kwargs
    ):
        async with create_session(session) as session:
            obj = model(**kwargs)
            session.add(obj)
            await session.flush()
            await session.refresh(obj)
            if commit:
                await session.commit()
            return obj

    async def update(
            self,
            model,
            condition,
            session=None,
            commit=True,
            many=False,
            **kwargs
    ):
        async with create_session(session) as session:
            query = update(model).where(condition).returning(
                *model.__table__.columns
            ).values(**kwargs)
            result = await session.execute(query)
            fields = result.keys()
            if many:
                result = [model(**dict(zip(fields, obj))) for obj in result]
            else:
                obj = result.first()
                result = model(**dict(zip(fields, obj))) if obj else None
            if commit:
                await session.commit()
            return result

    async def delete(
            self,
            model,
            condition,
            session=None,
            commit=True
    ):
        async with create_session(session) as session:
            await session.execute(delete(model).where(condition))
            if commit:
                await session.commit()
