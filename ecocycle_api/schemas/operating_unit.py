from typing import Optional
from pydantic import BaseModel, Field

from odoo.addons.ecocycle_api.schemas.base import OdooEntity, RelatedOdooEntity
from odoo.addons.ecocycle_api.schemas.res_partner import ResPartnerAddress


class OperatingUnit(OdooEntity):
    code: str = Field(serialization_alias="code")
    name: str = Field(serialization_alias="name")
    partner_id: ResPartnerAddress = Field(serialization_alias="address")
    
