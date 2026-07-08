from typing import Optional
from pydantic import BaseModel, Field

from odoo.addons.ecocycle_api.schemas.base import OdooEntity, RelatedOdooEntity


class ResPartnerAddress(OdooEntity):
    name: str = Field(serialization_alias="name")
    parent_id: Optional[RelatedOdooEntity] = Field(serialization_alias="parent_id")
    phone: Optional[str] = Field(serialization_alias="phone")
    street: Optional[str] = Field(serialization_alias="street")
    city: Optional[str] = Field(serialization_alias="city")
    state_id: Optional[RelatedOdooEntity] = Field(serialization_alias="state_id")
    country_id: Optional[RelatedOdooEntity] = Field(serialization_alias="country_id")
    zip: Optional[str] = Field(serialization_alias="zip")


class ResPartner(OdooEntity):
    name: str = Field(serialization_alias="name")
    email: str = Field(serialization_alias="email")
    phone: Optional[str] = Field(serialization_alias="phone")
    firebase_uuid: str = Field(serialization_alias="firebase_uuid")
    current_ou_id: Optional[RelatedOdooEntity] = Field(serialization_alias="current_ou_id")
    total_coin: float = Field(serialization_alias="total_coin")
    total_point: float = Field(serialization_alias="total_point")
    is_already_daily_checkin: bool = Field(serialization_alias="is_already_daily_checkin")
    last_daily_check_on: int = Field(serialization_alias="last_daily_check_on")
    child_ids: Optional[list[ResPartnerAddress]] = Field(serialization_alias="address")
    

class ResPartnerPostBody(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None
    firebase_uuid: str
    
    
class ResPartnerPutBody(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    current_ou_id: Optional[str] = None
    
    
class ResPartnerAddressPostBody(BaseModel):
    name: str
    parent_id: str
    phone: Optional[str] = None
    street: str
    city: str
    state_id: str
    country_id: str
    zip: Optional[str] = None
    
    
class ResPartnerAddressPutBody(BaseModel):
    name: Optional[str] = None
    parent_id: Optional[str] = None
    phone: Optional[str] = None
    street: Optional[str] = None
    city: Optional[str] = None
    state_id: Optional[str] = None
    country_id: Optional[str] = None
    zip: Optional[str] = None


class ResCountry(OdooEntity):
    name: str = Field(serialization_alias="name")
    
class ResCountryState(OdooEntity):
    name: str = Field(serialization_alias="name")
    country_id: RelatedOdooEntity = Field(serialization_alias="country_id")
    
class ResCountryStateQuery(BaseModel):
    name: Optional[str] = None
    country_id: Optional[str] = None
    