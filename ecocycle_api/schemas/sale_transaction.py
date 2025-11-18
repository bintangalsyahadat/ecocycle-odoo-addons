from typing import Optional
from datetime import datetime, timezone
from pydantic import BaseModel, Field

from odoo.addons.ecocycle_api.schemas.base import OdooEntity, RelatedOdooEntity, APIRequestBody

    

class SalesTransaction(OdooEntity):
    name: str = Field(serialization_alias="name")
    date: datetime = Field(serialization_alias="date")
    partner_id: RelatedOdooEntity = Field(serialization_alias="partner_id")
    operating_unit_id: RelatedOdooEntity = Field(serialization_alias="operating_unit_id")
    total_amount: float = Field(serialization_alias="total_amount")
    picking_ids: Optional[list[RelatedOdooEntity]] = Field(serialization_alias="picking_ids")
    delivery_method_id: RelatedOdooEntity = Field(serialization_alias="delivery_method_id")
    delivery_address_id: Optional[RelatedOdooEntity] = Field(serialization_alias="delivery_address_id")
    is_self_service: Optional[bool] = Field(serialization_alias="is_self_service")
    payment_method_id: RelatedOdooEntity = Field(serialization_alias="payment_method_id")
    payment_ids: Optional[list[RelatedOdooEntity]] = Field(serialization_alias="payment_ids")
    state: str = Field(serialization_alias="state")
    note: Optional[str] = Field(serialization_alias="note")
    
    
class SalesTransactionItem(OdooEntity):
    sale_transaction_id: RelatedOdooEntity = Field(serialization_alias="sale_transaction_id")
    waste_category_id: RelatedOdooEntity = Field(serialization_alias="waste_category_id")
    quantity: float = Field(serialization_alias="qty")
    unit_price: float = Field(serialization_alias="unit_price")
    total_price: float = Field(serialization_alias="total_price")
    operating_unit_id: RelatedOdooEntity = Field(serialization_alias="operating_unit_id")
    

class SalesTransactionDetail(SalesTransaction):
    line_ids: Optional[list[SalesTransactionItem]] = Field(serialization_alias="line_ids")
    

class SalesTransactionItemPostBody(APIRequestBody):
    waste_category_id: str
    quantity: float
    

class SalesTransactionPostBody(APIRequestBody):
    date: datetime
    partner_id: str
    operating_unit_id: str
    delivery_method_id: str
    delivery_address_id: Optional[str]
    payment_method_id: str
    note: Optional[str]
    line_ids: list[SalesTransactionItemPostBody]
    
