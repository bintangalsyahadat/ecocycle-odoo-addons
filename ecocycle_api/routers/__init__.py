from fastapi import APIRouter

from ..schemas.base import ValidationErrorResponse

ecocycle_router = APIRouter(
    responses={422: {"model": ValidationErrorResponse}})

from .resource import resource_router
from .purchase_transaction import purchase_transaction_router
from .sale_transaction import sale_transaction_router
from .planner import planner_router

ecocycle_router.include_router(resource_router)
ecocycle_router.include_router(purchase_transaction_router)
ecocycle_router.include_router(sale_transaction_router)
ecocycle_router.include_router(planner_router)