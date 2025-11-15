from typing import Optional
from pydantic import BaseModel, Field

from odoo.addons.ecocycle_api.schemas.base import OdooEntity, RelatedOdooEntity


class ResPartner(OdooEntity):
    name: str = Field(serialization_alias="name")
    email: str = Field(serialization_alias="email")
    firebase_uuid: str = Field(serialization_alias="firebase_uuid")
    current_ou_id: Optional[RelatedOdooEntity] = Field(serialization_alias="current_ou_id")
    
class ResPartnerPostBody(BaseModel):
    name: str
    email: str
    firebase_uuid: str
    
    
class ResPartnerPutBody(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    current_ou_id: Optional[str] = None
    