from typing import Annotated, Optional

from fastapi import APIRouter, Depends, HTTPException

from odoo.api import Environment

from odoo.addons.fastapi.dependencies import odoo_env
from odoo.addons.ecocycle_api.schemas.base import PaginatedRecords, PaginationParams, SingleRecord
from odoo.addons.ecocycle_api.utils.records import fetch_record, fetch_recordset
from odoo.addons.ecocycle_api.dependencies import paginator, auth_jwt_authenticated_odoo_env
from ..schemas.base import SearchQuery
from ..schemas.res_partner import ResPartner, ResPartnerPostBody, ResPartnerPutBody
from ..schemas.operating_unit import OperatingUnit
from ..schemas.waste_category import WasteCategory, WasteCategoryStock, WasteCategoryStockBody
from ..schemas.delivery_method import DeliveryMethod
from ..schemas.payment_method import PaymentMethod

resource_router = APIRouter(tags=["Resource"])
    

@resource_router.get("/res/user/{api_id}", response_model=SingleRecord[ResPartner])
def get_user(
    env: Annotated[Environment, Depends(auth_jwt_authenticated_odoo_env)],
    api_id: str,
) -> Optional[SingleRecord[ResPartner]]:
    """Get User Detail"""

    domain = ['|', ('firebase_uuid', "=", api_id), ("api_id", "=", api_id)]

    return fetch_record(
        env=env,
        base_domain=[("active", "=", True)],
        domain=domain,
        model="res.partner",
        schema_model=ResPartner,
    )
    

@resource_router.post("/res/user/create", response_model=SingleRecord[ResPartner])
def create_user(
    body: ResPartnerPostBody,
    env: Annotated[Environment, Depends(auth_jwt_authenticated_odoo_env)],
) -> Optional[SingleRecord[ResPartner]]:
    """Create User"""

    user = env['res.partner'].search(
        [('firebase_uuid', '=', body.firebase_uuid)], limit=1)
    if not user:
        user = env['res.partner']._create_api_record(body)
        
        
    return SingleRecord[ResPartner](
        result=ResPartner.model_validate(user),
    )


@resource_router.put("/res/user/{api_id}", response_model=SingleRecord[ResPartner])
def update_user(
    env: Annotated[Environment, Depends(auth_jwt_authenticated_odoo_env)],
    api_id: str,
    body: ResPartnerPutBody,
) -> Optional[SingleRecord[ResPartner]]:
    """Update User"""

    domain = ['|', ("api_id", "=", api_id), ("firebase_uuid", "=", api_id)]
    partner = env['res.partner'].search(domain)
    if not partner:
        raise HTTPException(status_code=404, detail="Record not found")

    partner = partner.with_context(
        by_alias=False)._update_api_record(partner.api_id, body)
    
    return SingleRecord[ResPartner](
        result=ResPartner.model_validate(partner),
    )
    

@resource_router.post("/res/user/{api_id}/check")
def user_daily_check(
    api_id: str,
    env: Annotated[Environment, Depends(auth_jwt_authenticated_odoo_env)],
):
    
    domain = ['|', ('api_id', '=', api_id), ('firebase_uuid', '=', api_id)]
    user = env['res.partner'].search(domain, limit=1)
    daily_check = user.sudo().action_daily_check() or False
    
    return {
        'success': daily_check
    }


@resource_router.get("/res/operating-units", response_model=PaginatedRecords[OperatingUnit])
def get_operating_units(
    env: Annotated[Environment, Depends(auth_jwt_authenticated_odoo_env)],
    paging: Annotated[PaginationParams, Depends(paginator)],
    query_params: Annotated[SearchQuery, Depends()],
) -> PaginatedRecords[OperatingUnit]:
    """Get Operating Unit list"""

    domain = []
    if query_params.q:
        domain.append(("name", "ilike", query_params.q))

    return fetch_recordset(
        env=env,
        paging=paging,
        base_domain=[],
        domain=domain,
        model="operating.unit",
        schema_model=OperatingUnit,
    )

@resource_router.get("/res/categories", response_model=PaginatedRecords[WasteCategory])
def get_categories(
    env: Annotated[Environment, Depends(auth_jwt_authenticated_odoo_env)],
    paging: Annotated[PaginationParams, Depends(paginator)],
    query_params: Annotated[SearchQuery, Depends()],
) -> PaginatedRecords[WasteCategory]:
    """Get Category list"""

    domain = []
    if query_params.q:
        domain.append(("name", "ilike", query_params.q))

    return fetch_recordset(
        env=env,
        paging=paging,
        base_domain=[],
        domain=domain,
        model="waste.category",
        schema_model=WasteCategory,
    )
    

@resource_router.post("/res/category/stock", response_model=WasteCategoryStock)
def get_category_stock(
    body: WasteCategoryStockBody,
    env: Annotated[Environment, Depends(auth_jwt_authenticated_odoo_env)],
):
    
    category = env['waste.category'].search([('api_id', '=', body.category_id)], limit=1)
    operating_unit = env['operating.unit'].search([('api_id', '=', body.operating_unit_id)], limit=1)
    
    stock = category.sudo().get_stock(operating_unit)
    return {
        'qty_forecasted': stock['qty_forecasted'],
        'operating_unit_id': {
            "api_id": operating_unit.api_id,
            "display_name": operating_unit.display_name
        }
    }


@resource_router.get("/res/delivery-method", response_model=PaginatedRecords[DeliveryMethod])
def get_delivery_method(
    env: Annotated[Environment, Depends(auth_jwt_authenticated_odoo_env)],
    paging: Annotated[PaginationParams, Depends(paginator)],
    query_params: Annotated[SearchQuery, Depends()],
) -> PaginatedRecords[DeliveryMethod]:
    """Get Delivery Method list"""

    domain = []
    if query_params.q:
        domain.append(("name", "ilike", query_params.q))

    return fetch_recordset(
        env=env,
        paging=paging,
        base_domain=[],
        domain=domain,
        model="ecocycle.delivery.method",
        schema_model=DeliveryMethod,
    )

@resource_router.get("/res/payment-method", response_model=PaginatedRecords[PaymentMethod])
def get_payment_method(
    env: Annotated[Environment, Depends(auth_jwt_authenticated_odoo_env)],
    paging: Annotated[PaginationParams, Depends(paginator)],
    query_params: Annotated[SearchQuery, Depends()],
) -> PaginatedRecords[PaymentMethod]:
    """Get Payment Method list"""

    domain = []
    if query_params.q:
        domain.append(("name", "ilike", query_params.q))

    return fetch_recordset(
        env=env,
        paging=paging,
        base_domain=[],
        domain=domain,
        model="ecocycle.payment.method",
        schema_model=PaymentMethod,
    )


