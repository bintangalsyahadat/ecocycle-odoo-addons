# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from starlette.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware

_logger = logging.getLogger(__name__)


class FastapiEndpoint(models.Model):
    _inherit = 'fastapi.endpoint'

    app = fields.Selection(
        selection_add=[("ecocycle", "EcoCycle Endpoint")], ondelete={"ecocycle": "cascade"}
    )

    def _get_fastapi_routers(self):
        if self.app == "ecocycle":
            from ..routers import ecocycle_router
            return [ecocycle_router]
        return super()._get_fastapi_routers()
