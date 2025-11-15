from typing import Annotated, Optional

from fastapi import APIRouter, Depends

from odoo.api import Environment

from odoo.addons.fastapi.dependencies import odoo_env
from odoo.addons.ecocycle_api.schemas.base import PaginatedRecords, PaginationParams, SingleRecord
from odoo.addons.ecocycle_api.utils.records import fetch_record, fetch_recordset
from odoo.addons.ecocycle_api.dependencies import paginator, auth_jwt_authenticated_odoo_env
from ..schemas.base import SearchQuery
from ..schemas.res_partner import ResPartner, ResPartnerPostBody
from ..schemas.operating_unit import OperatingUnit
from ..schemas.waste_category import WasteCategory, WasteCategoryStock, WasteCategoryStockBody
from ..schemas.delivery_method import DeliveryMethod
from ..schemas.payment_method import PaymentMethod

resource_router = APIRouter(tags=["Resource"])
    

@resource_router.get("/res/user/{firebase_uuid}", response_model=SingleRecord[ResPartner])
def get_user(
    env: Annotated[Environment, Depends(auth_jwt_authenticated_odoo_env)],
    firebase_uuid: str,
) -> Optional[SingleRecord[ResPartner]]:
    """Get User Detail"""

    domain = ['|', ('firebase_uuid', "=", firebase_uuid), ("api_id", "=", firebase_uuid)]

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
):
    """Create User"""

    user = env['res.partner'].search(
        [('firebase_uuid', '=', body.firebase_uuid)], limit=1)
    if not user:
        user = env['res.partner']._create_api_record(body)
        
        
    return SingleRecord[ResPartner](
        result=ResPartner.model_validate(user),
    )


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


