from typing import Optional
from datetime import datetime, timezone
from pydantic import BaseModel, Field

from odoo.addons.ecocycle_api.schemas.base import OdooEntity, RelatedOdooEntity, APIRequestBody
from odoo.addons.ecocycle_api.schemas.res_partner import ResPartner, ResPartnerAddress
from odoo.addons.ecocycle_api.schemas.delivery_method import DeliveryMethod


class PurchaseTransaction(OdooEntity):
    name: str = Field(serialization_alias="name")
    date: datetime = Field(serialization_alias="date")
    scheduled_date: Optional[datetime] = Field(
        serialization_alias="scheduled_date")
    partner_id: ResPartner = Field(serialization_alias="partner_id")
    operating_unit_id: RelatedOdooEntity = Field(
        serialization_alias="operating_unit_id")
    estimate_total_amount: float = Field(
        serialization_alias="estimate_total_amount")
    total_amount: float = Field(serialization_alias="total_amount")
    picking_ids: Optional[list[RelatedOdooEntity]] = Field(
        serialization_alias="picking_ids")
    delivery_method_id: DeliveryMethod = Field(
        serialization_alias="delivery_method_id")
    delivery_address_id: Optional[ResPartnerAddress] = Field(
        serialization_alias="delivery_address_id")
    is_self_service: Optional[bool] = Field(
        serialization_alias="is_self_service")
    state: str = Field(serialization_alias="state")
    note: Optional[str] = Field(serialization_alias="note")


class PurchaseTransactionItem(OdooEntity):
    purchase_transaction_id: RelatedOdooEntity = Field(
        serialization_alias="purchase_transaction_id")
    waste_category_id: RelatedOdooEntity = Field(
        serialization_alias="waste_category_id")
    quantity: float = Field(serialization_alias="qty")
    unit_price: float = Field(serialization_alias="unit_price")
    estimate_total_price: float = Field(
        serialization_alias="estimate_total_price")
    total_price: float = Field(serialization_alias="total_price")
    valid_qty: float = Field(serialization_alias="valid_qty")
    operating_unit_id: RelatedOdooEntity = Field(
        serialization_alias="operating_unit_id")


class PurchaseTransactionDetail(PurchaseTransaction):
    line_ids: Optional[list[PurchaseTransactionItem]
                       ] = Field(serialization_alias="line_ids")


class PurchaseTransactionItemPostBody(APIRequestBody):
    waste_category_id: str
    quantity: float


class PurchaseTransactionPostBody(APIRequestBody):
    date: datetime
    partner_id: str
    operating_unit_id: str
    delivery_method_id: str
    delivery_address_id: Optional[str]
    note: Optional[str]
    line_ids: list[PurchaseTransactionItemPostBody]
