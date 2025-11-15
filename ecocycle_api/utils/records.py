from datetime import timezone
from typing import Optional, Type
from fastapi import HTTPException

from odoo.api import Environment
from odoo.models import BaseModel

from ..schemas.base import T, PaginatedRecords, PaginationParams, SingleRecord, PaginationMeta


# =========================================================
#  Generic Record Browsing Utilities
# =========================================================
def find_record(
    env: Environment,
    model: str,
    uid_ref: str,
    use_sudo: bool = False,
    raise_if_missing: bool = True,
) -> Optional[BaseModel]:
    """
    Retrieve a single record of any Odoo model using its unique API reference.
    """
    model_obj = env[model]
    if use_sudo:
        model_obj = model_obj.sudo()

    rec = model_obj.search([("api_id", "=", uid_ref)], limit=1)
    if not rec and raise_if_missing:
        raise HTTPException(status_code=404, detail="Record not found")

    return rec


def fetch_record(
    env: Environment,
    base_domain: list,
    model: str,
    schema_model: Type[T],
    domain: Optional[list] = None,
    use_sudo: bool = False,
    ctx: Optional[dict] = None,
) -> SingleRecord:
    """
    Fetch a single record and return it as a Pydantic response model.
    """
    model_obj = env[model]
    if not hasattr(model_obj, "_fetch_api_records"):
        raise HTTPException(
            status_code=500,
            detail=f"Model {model} does not implement _fetch_api_records method",
        )

    if use_sudo:
        model_obj = model_obj.sudo()
    if ctx:
        model_obj = model_obj.with_context(**ctx)

    params = dict(domain=domain)
    recs, total = getattr(model_obj, "_fetch_api_records")(
        base_domain=base_domain,
        search_params=params,
    )
    if not recs:
        raise HTTPException(status_code=404, detail="Record not found")

    return SingleRecord[schema_model](result=schema_model.model_validate(recs))


def fetch_recordset(
    env: Environment,
    paging: PaginationParams,
    base_domain: list,
    model: str,
    schema_model: Type[T],
    domain: Optional[list] = None,
    use_sudo: bool = False,
    ctx: Optional[dict] = None,
) -> PaginatedRecords:
    """
    Retrieve a list of records from any model with pagination support.
    """
    model_obj = env[model]
    if not hasattr(model_obj, "_fetch_api_records"):
        raise HTTPException(
            status_code=500,
            detail=f"Model {model} does not implement _fetch_api_records method",
        )

    if use_sudo:
        model_obj = model_obj.sudo()
    if ctx:
        model_obj = model_obj.with_context(**ctx)

    params = dict(paging.model_dump(exclude={"page_number"}), domain=domain)
    recs, total = getattr(model_obj, "_fetch_api_records")(
        base_domain=base_domain,
        search_params=params,
    )

    return PaginatedRecords(
        result=[schema_model.model_validate(r) for r in recs],
        result_info=PaginationMeta(
            page=paging.page_number or 1,
            per_page=paging.limit or 80,
            count=len(recs),
            total_count=total,
        ),
    )


# =========================================================
#  Field Conversion Helpers
# =========================================================
def map_relational_field(
    env,
    values: dict,
    source_field: str,
    model: str,
    target_field: Optional[str] = None,
    as_command: bool = False,
):
    """
    Resolve a relational field (many2one / many2many) by API reference.
    """
    uid_ref = values.pop(source_field, None)
    if uid_ref:
        rec = find_record(env, model, uid_ref, raise_if_missing=False)
        if rec:
            if as_command:
                values[target_field or source_field] = [(6, 0, rec.ids)]
            else:
                values[target_field or source_field] = rec.id


def normalize_datetime_field(values: dict, src_field: str, target_field: Optional[str] = None):
    """
    Normalize a datetime field to UTC without tzinfo for consistent storage.
    """
    values[target_field or src_field] = (
        values[src_field].astimezone(timezone.utc).replace(tzinfo=None)
    )
