from typing import Optional
from pydantic import BaseModel, Field

from odoo.addons.ecocycle_api.schemas.base import OdooEntity, RelatedOdooEntity


class DeliveryMethod(OdooEntity):
    name: str = Field(serialization_alias="name")
    description: str = Field(serialization_alias="description")
    type: str = Field(serialization_alias="type")
