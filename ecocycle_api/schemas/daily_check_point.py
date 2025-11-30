from typing import Optional
from pydantic import BaseModel, Field

from odoo.addons.ecocycle_api.schemas.base import OdooEntity, RelatedOdooEntity


class DailyCheckPoint(OdooEntity):
    name: str = Field(serialization_alias="name")
    sequence: int = Field(serialization_alias="sequence")
    point: Optional[float] = Field(serialization_alias="point")
    rendom_point_start: Optional[float] = Field(serialization_alias="rendom_point_start")
    rendom_point_end: Optional[float] = Field(serialization_alias="rendom_point_end")
    is_random: Optional[bool] = Field(serialization_alias="is_random")
    
