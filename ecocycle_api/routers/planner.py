from typing import Annotated, Optional

from fastapi import APIRouter, Depends, HTTPException

from odoo.api import Environment

from odoo.addons.fastapi.dependencies import odoo_env
from odoo.addons.ecocycle_api.schemas.base import PaginatedRecords, PaginationParams, SingleRecord
from odoo.addons.ecocycle_api.utils.records import fetch_record, fetch_recordset
from odoo.addons.ecocycle_api.dependencies import paginator, auth_jwt_authenticated_odoo_env
from ..schemas.planner import Planner, PlannerPostBody, PlannerSearchQuery

planner_router = APIRouter(tags=["Planner"])


@planner_router.get("/planer", response_model=PaginatedRecords[Planner])
def get_planner(
    env: Annotated[Environment, Depends(auth_jwt_authenticated_odoo_env)],
    paging: Annotated[PaginationParams, Depends(paginator)],
    query_params: Annotated[PlannerSearchQuery, Depends()],
) -> PaginatedRecords[Planner]:
    """Get Planner List"""

    domain = []
    if query_params.date:
        domain.append(("date", "=", query_params.date))
    if query_params.state:
        domain.append(("state", "=", query_params.state))
    if query_params.partner_id:
        partner = env['res.partner'].search(['|', ('api_id', '=', query_params.partner_id), ('firebase_uuid', '=', query_params.partner_id)], limit=1)
        domain.append(("partner_id", "=", partner.id))

    return fetch_recordset(
        env=env,
        paging=paging,
        base_domain=[],
        domain=domain,
        model="ecocycle.planner",
        schema_model=Planner,
    )


@planner_router.post("/planner", response_model=SingleRecord[Planner])
def create_planner(
    body: PlannerPostBody,
    env: Annotated[Environment, Depends(auth_jwt_authenticated_odoo_env)],
) -> Optional[SingleRecord[Planner]]:
    """Create Planner"""

    planner = env['ecocycle.planner']._create_api_record(body)
        
    return SingleRecord[Planner](
        result=Planner.model_validate(planner),
    )
