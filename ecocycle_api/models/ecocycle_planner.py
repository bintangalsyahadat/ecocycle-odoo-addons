import logging
from typing import Optional

from odoo import api, fields, models
from odoo.addons.ecocycle_api.utils.records import map_relational_field, normalize_datetime_field, find_record
from odoo.addons.ecocycle_api.schemas.planner import PlannerPostBody 

class EcoCyclePlanner(models.Model):
    _name = 'ecocycle.planner'
    _inherit = ['ecocycle.planner', 'api.resource']
    
    @api.model
    def _prepare_api_values(
        self,
        body: Optional[PlannerPostBody] = None,
        vals: Optional[dict] = None
    ):
        vals = super()._prepare_api_values(body, vals)
        map_relational_field(self.env, vals, 'partner_id', 'res.partner')
    
        return vals
    