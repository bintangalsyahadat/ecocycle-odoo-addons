from typing import Optional
from pydantic import BaseModel, Field

from odoo.addons.ecocycle_api.schemas.base import OdooEntity, RelatedOdooEntity


class WasteCategory(OdooEntity):
    name: str = Field(serialization_alias="name")
    description: str = Field(serialization_alias="description")
    image: Optional[str] = Field(serialization_alias="image")


class WasteCategoryStock(BaseModel):
    success: bool = True
    qty_forecasted: float
    operating_unit_id: RelatedOdooEntity
    
    
class WasteCategoryStockBody(BaseModel):
    category_id: str
    operating_unit_id: str