from typing import TypeVar, Generic, Union, Optional, Any, Type
from pydantic import BaseModel, Field, model_validator
from extendable_pydantic.models import ExtendableBaseModel, StrictExtendableBaseModel
from datetime import datetime, timezone
from odoo import fields
from odoo.models import BaseModel as OdooModel

T = TypeVar("T", bound=BaseModel)


def extract_odoo_record(model: Any, record: OdooModel) -> dict:
    """
    Transform an Odoo record into a dictionary compatible with
    a given Pydantic model definition.

    Args:
        model: Pydantic model class to shape the result.
        record: Odoo model instance.

    Returns:
        dict containing field values converted according to Odoo field types.
    """
    output = {}

    for name, field_info in model.model_fields.items():
        odoo_field_name = field_info.alias or name
        value = getattr(record, odoo_field_name, None)

        if hasattr(record, "_fields") and name in record._fields:
            odoo_field = record._fields[name]
            field_type = odoo_field.type

            if value is False and field_type != "boolean":
                value = None
            elif field_type == "date" and not value:
                value = None
            elif field_type == "datetime":
                if value:
                    value = fields.Datetime.context_timestamp(record, value)
                else:
                    value = None
            elif field_type == "many2one":
                value = value or None
            elif field_type in ("one2many", "many2many"):
                value = list(value) if value else []

        output[name] = value
    return output


# --------------------------
# Base Response Definitions
# --------------------------

class APIResponse(BaseModel):
    success: bool = True
    message: str = "OK"


class SingleRecord(APIResponse, Generic[T]):
    result: T


class MultipleRecords(APIResponse, Generic[T]):
    result: list[T]


class PaginationMeta(BaseModel):
    page: int
    per_page: int
    count: int
    total_count: int


class PaginatedRecords(MultipleRecords, Generic[T]):
    result_info: PaginationMeta


class PaginationParams(BaseModel):
    limit: Optional[int]
    offset: Optional[int]
    page_number: Optional[int]


class ValidationErrorResponse(APIResponse):
    success: bool = False
    message: str = "Validation Error"
    result: dict[str, str] = Field(
        examples=[{
            "field_name_1": "This field is required.",
            "field_name_2": "Must be a valid email address."
        }]
    )


# --------------------------
# Odoo Model Conversion
# --------------------------

class OdooEntity(BaseModel, revalidate_instances="always"):
    api_id: str = Field(serialization_alias="id")
    create_date: Optional[datetime] = Field(serialization_alias="created_at")
    write_date: Optional[datetime] = Field(serialization_alias="updated_at")

    model_config = {
        "from_attributes": True,
        "json_encoders": {
            datetime: lambda v: (
                v.isoformat() if v.tzinfo
                else v.replace(tzinfo=timezone.utc).isoformat()
            )
        },
    }

    @model_validator(mode="before")
    def from_odoo_record(cls, raw_data: Any) -> Any:
        if isinstance(raw_data, OdooModel):
            return extract_odoo_record(cls, raw_data)
        return raw_data


class RelatedOdooEntity(BaseModel):
    api_id: Optional[str] = Field(default=None, serialization_alias="id")
    display_name: Optional[str] = Field(default=None, serialization_alias="name")

    model_config = {"from_attributes": True}

    @model_validator(mode="before")
    def from_odoo_record(cls, raw_data: Any) -> Any:
        if isinstance(raw_data, OdooModel):
            return extract_odoo_record(cls, raw_data)
        return raw_data


class APIRequestBody(ExtendableBaseModel, revalidate_instances="always"):
    """Base model for incoming request payloads."""
    pass


class SearchQuery(BaseModel):
    q: Optional[str] = None
