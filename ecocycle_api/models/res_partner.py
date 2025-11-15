# -*- coding: utf-8 -*-
import logging
from typing import Optional

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

from ..utils import map_relational_field, normalize_datetime_field, find_record
from ..schemas.res_partner import ResPartnerPutBody

_logger = logging.getLogger(__name__)

class ResPartner(models.Model):
    _name = 'res.partner'
    _inherit = ['res.partner', 'api.resource']
    
    @api.model
    def _prepare_api_values(
        self,
        body: Optional[ResPartnerPutBody] = None,
        vals: Optional[dict] = None
    ):
        vals = super()._prepare_api_values(body, vals)
        map_relational_field(self.env, vals, 'current_ou_id', 'operating.unit')

        return vals
