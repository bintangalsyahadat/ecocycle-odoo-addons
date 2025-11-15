from typing import Annotated

from fastapi import Query, Depends
from odoo.addons.base.models.res_partner import Partner

from odoo.addons.fastapi_auth_jwt.dependencies import auth_jwt_authenticated_partner
from odoo.api import Environment
from .schemas.base import PaginationParams


def auth_jwt_authenticated_odoo_env(
    partner: Annotated[Partner, Depends(auth_jwt_authenticated_partner)]
) -> Environment:
    user = partner.sudo().user_ids
    env = partner.with_user(user).with_context(authenticated_partner_id=partner.id).env
    return env


def paginator(
    page: Annotated[int, Query(ge=1)] = 1,
    page_size: Annotated[int, Query(ge=1)] = 80
) -> PaginationParams:
    """Return a PaginationParams object from the page and page_size parameters"""
    return PaginationParams(limit=page_size, offset=(page - 1) * page_size, page_number=page)
