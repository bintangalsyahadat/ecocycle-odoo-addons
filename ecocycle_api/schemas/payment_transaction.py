from typing import Optional
from datetime import date as dt, datetime
from pydantic import BaseModel, Field

from odoo.addons.ecocycle_api.schemas.base import OdooEntity, RelatedOdooEntity


class PaymentTransaction(OdooEntity):
    memo: Optional[str] = Field(serialization_alias="memo")
    date: dt = Field(serialization_alias="date")
    payment_date: Optional[datetime] = Field(serialization_alias="payment_date")
    partner_id: RelatedOdooEntity = Field(serialization_alias="partner_id")
    operating_unit_id: RelatedOdooEntity = Field(serialization_alias="operating_unit_id")
    amount: Optional[float] = Field(serialization_alias="amount")
    payment_method_id: RelatedOdooEntity = Field(serialization_alias="payment_method_id")
    state: str = Field(serialization_alias="state")
    sale_transaction_id: Optional[RelatedOdooEntity] = Field(serialization_alias="sale_transaction_id")
    xendit_invoice_id: Optional[str] = Field(serialization_alias="xendit_invoice_id")
    xendit_checkout_url: Optional[str] = Field(serialization_alias="xendit_checkout_url")
    xendit_expired_date: Optional[datetime] = Field(serialization_alias="xendit_expired_date")   
     
