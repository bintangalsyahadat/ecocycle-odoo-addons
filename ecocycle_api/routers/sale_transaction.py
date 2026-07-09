from typing import Annotated, Optional

from fastapi import APIRouter, Depends, HTTPException

from odoo.api import Environment

from odoo.addons.fastapi.dependencies import odoo_env
from odoo.addons.ecocycle_api.schemas.base import PaginatedRecords, PaginationParams, SingleRecord
from odoo.addons.ecocycle_api.utils.records import fetch_record, fetch_recordset
from odoo.addons.ecocycle_api.dependencies import paginator, auth_jwt_authenticated_odoo_env
from ..schemas.base import SearchQuery
from ..schemas.sale_transaction import SalesTransaction, SalesTransactionPostBody, SalesTransactionDetail

sale_transaction_router = APIRouter(tags=["Sales Transaction"])


@sale_transaction_router.get("/sale/{user_id}", response_model=PaginatedRecords[SalesTransaction])
def get_sale_transaction_user(
    env: Annotated[Environment, Depends(auth_jwt_authenticated_odoo_env)],
    user_id: str,
    paging: Annotated[PaginationParams, Depends(paginator)],
    query_params: Annotated[SearchQuery, Depends()],
) -> PaginatedRecords[SalesTransaction]:
    """Get Sales Transaction User list"""

    domain = []
    if query_params.q:
        domain.append(("name", "ilike", query_params.q))

    partner = env['res.partner'].search(['|', ('api_id', '=', user_id), ('firebase_uuid', '=', user_id)], limit=1)
    domain.append(("partner_id", "=", partner.id))

    return fetch_recordset(
        env=env,
        paging=paging,
        base_domain=[],
        domain=domain,
        model="sale.transaction",
        schema_model=SalesTransaction,
    )


@sale_transaction_router.get("/sale/{user_id}/{api_id}", response_model=SingleRecord[SalesTransactionDetail])
def get_sale_transaction_user_detail(
    env: Annotated[Environment, Depends(auth_jwt_authenticated_odoo_env)],
    user_id: str,
    api_id: str,
) -> Optional[SingleRecord[SalesTransactionDetail]]:
    """Get Sales Transaction User Detail"""

    domain = ['|', ("api_id", "=", api_id), ("name", "=", api_id)]
    partner = env['res.partner'].search(['|', ('api_id', '=', user_id), ('firebase_uuid', '=', user_id)], limit=1)

    return fetch_record(
        env=env,
        base_domain=[("partner_id", "=", partner.id)],
        domain=domain,
        model="sale.transaction",
        schema_model=SalesTransactionDetail,
    )
    

@sale_transaction_router.post("/sale/create", response_model=SingleRecord[SalesTransactionDetail])
def create_sale(
    env: Annotated[Environment, Depends(auth_jwt_authenticated_odoo_env)],
    body: SalesTransactionPostBody,
) -> Optional[SingleRecord[SalesTransactionDetail]]:
    """Create Sale Transaction"""

    sale = env['sale.transaction']._create_api_record(body)
    sale.sudo().action_confirm()
    return SingleRecord[SalesTransactionDetail](
        result=SalesTransactionDetail.model_validate(sale),
    )


@sale_transaction_router.put("/sale/{user_id}/{api_id}/receive", response_model=SingleRecord[SalesTransactionDetail])
def receive_sale(
    env: Annotated[Environment, Depends(auth_jwt_authenticated_odoo_env)],
    user_id: str,
    api_id: str,
) -> Optional[SingleRecord[SalesTransactionDetail]]:
    """User confirms receipt of delivered order (on_delivery → sale)"""

    partner = env['res.partner'].search(
        ['|', ('api_id', '=', user_id), ('firebase_uuid', '=', user_id)], limit=1)
    domain = ['|', ("api_id", "=", api_id), ("name", "=", api_id)]
    domain.append(("partner_id", "=", partner.id))
    domain.append(("state", "=", "on_delivery"))

    sale = env['sale.transaction'].search(domain, limit=1)
    if not sale:
        raise HTTPException(status_code=404, detail="No on-delivery order found")

    sale.sudo().action_receive()
    return SingleRecord[SalesTransactionDetail](
        result=SalesTransactionDetail.model_validate(sale),
    )
    


