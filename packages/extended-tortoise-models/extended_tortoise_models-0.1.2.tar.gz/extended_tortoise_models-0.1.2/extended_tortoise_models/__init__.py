from uuid import UUID

from tortoise import Model, fields


class UuidModel(Model):
    id: UUID = fields.UUIDField(pk=True)

    class Meta:
        abstract = True
