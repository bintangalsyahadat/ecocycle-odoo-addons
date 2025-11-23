from typing import Optional
from pydantic import BaseModel, Field

from odoo.addons.ecocycle_api.schemas.base import OdooEntity, RelatedOdooEntity


class PaymentMethod(OdooEntity):
    name: str = Field(serialization_alias="name")
    description: Optional[str] = Field(serialization_alias="description")
