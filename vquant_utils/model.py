from datetime import datetime
from pymongo import DESCENDING


class MongoModel(object):
    fields = tuple()

    def __init__(self, database):
        self._table = getattr(database, type(self).__name__)

    async def find(self, **kwargs):
        return await self._table.find_one(kwargs)

    async def query(self, page=1, limit=20, order_by='created', desc=DESCENDING, **kwargs):
        skip_value = (page - 1) * limit
        skip_value = skip_value if skip_value > 0 else 0
        cursor = self._table.find(kwargs).sort(order_by, desc).skip(skip_value).limit(limit)
        return await cursor.to_list(limit)

    async def create(self, **kwargs):
        kwargs.update(dict(
            created=datetime.utcnow(),
            updated=datetime.utcnow()
        ))
        result = await self._table.insert_one(kwargs)
        return dict(_id=result.inserted_id)

    async def update(self, document, **kwargs):
        document.update(dict(
            updated=datetime.utcnow()
        ))
        result = await self._table.update_many(kwargs, {
            '$set': document
        })
        return result.raw_result.get('updatedExisting')

    async def delete(self, **kwargs):
        result = await self._table.delete_many(kwargs)
        return result.deleted_count > 0
