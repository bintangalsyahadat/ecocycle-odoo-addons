from typing import Optional
from pydantic import BaseModel, Field

from odoo.addons.ecocycle_api.schemas.base import OdooEntity, RelatedOdooEntity


class ResPartner(OdooEntity):
    name: str = Field(serialization_alias="name")
    email: str = Field(serialization_alias="email")
    firebase_uuid: str = Field(serialization_alias="firebase_uuid")
    
class ResPartnerPostBody(BaseModel):
    name: str
    email: str
    firebase_uuid: str
    