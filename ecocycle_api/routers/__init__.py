from fastapi import APIRouter

from ..schemas.base import ValidationErrorResponse

ecocycle_router = APIRouter(
    responses={422: {"model": ValidationErrorResponse}})

from .resource import resource_router

ecocycle_router.include_router(resource_router)