from typing import Optional
from pydantic import BaseModel, Field

from odoo.addons.ecocycle_api.schemas.base import OdooEntity, RelatedOdooEntity


class OperatingUnit(OdooEntity):
    code: str = Field(serialization_alias="code")
    name: str = Field(serialization_alias="name")
