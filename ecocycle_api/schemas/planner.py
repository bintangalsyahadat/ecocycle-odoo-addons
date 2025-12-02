from typing import Optional
from pydantic import BaseModel, Field
from datetime import date as dt

from odoo.addons.ecocycle_api.schemas.base import OdooEntity, RelatedOdooEntity
from odoo.addons.ecocycle_api.schemas.res_partner import ResPartner


class Planner(OdooEntity):
    date: dt = Field(serialization_alias="date")
    partner_id: ResPartner = Field(serialization_alias="partner_id")
    point_rewarded: float = Field(serialization_alias="point_rewarded")
    state: str = Field(serialization_alias="state")
    

class PlannerPostBody(BaseModel):
    date: dt = Field(serialization_alias="date")
    partner_id: str = Field(serialization_alias="partner_id")


class PlannerSearchQuery(BaseModel):
    date: Optional[dt] = None
    partner_id: Optional[str] = None
    state: Optional[str] = None
