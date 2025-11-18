from typing import Annotated, Optional

from fastapi import APIRouter, Depends, HTTPException

from odoo.api import Environment

from odoo.addons.fastapi.dependencies import odoo_env
from odoo.addons.ecocycle_api.schemas.base import PaginatedRecords, PaginationParams, SingleRecord
from odoo.addons.ecocycle_api.utils.records import fetch_record, fetch_recordset
from odoo.addons.ecocycle_api.dependencies import paginator, auth_jwt_authenticated_odoo_env
from ..schemas.base import SearchQuery
from ..schemas.purchase_transaction import PurchaseTransaction, PurchaseTransactionPostBody, PurchaseTransactionDetail

purchase_transaction_router = APIRouter(tags=["Purchase Transaction"])


@purchase_transaction_router.get("/purchase/{user_id}", response_model=PaginatedRecords[PurchaseTransaction])
def get_purchase_transaction_user(
    env: Annotated[Environment, Depends(auth_jwt_authenticated_odoo_env)],
    user_id: str,
    paging: Annotated[PaginationParams, Depends(paginator)],
    query_params: Annotated[SearchQuery, Depends()],
) -> PaginatedRecords[PurchaseTransaction]:
    """Get Purchase Transaction User list"""

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
        model="purchase.transaction",
        schema_model=PurchaseTransaction,
    )


@purchase_transaction_router.get("/purchase/{user_id}/{api_id}", response_model=SingleRecord[PurchaseTransactionDetail])
def get_purchase_transaction_user_detail(
    env: Annotated[Environment, Depends(auth_jwt_authenticated_odoo_env)],
    user_id: str,
    api_id: str,
) -> Optional[SingleRecord[PurchaseTransactionDetail]]:
    """Get Purchase Transaction User Detail"""

    domain = [("api_id", "=", api_id)]
    partner = env['res.partner'].search(['|', ('api_id', '=', user_id), ('firebase_uuid', '=', user_id)], limit=1)

    return fetch_record(
        env=env,
        base_domain=[("partner_id", "=", partner.id)],
        domain=domain,
        model="purchase.transaction",
        schema_model=PurchaseTransactionDetail,
    )