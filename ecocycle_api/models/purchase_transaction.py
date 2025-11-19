import logging
from typing import Optional

from odoo import api, fields, models

from odoo.addons.ecocycle_api.utils.records import map_relational_field, normalize_datetime_field, find_record
from odoo.addons.ecocycle_api.schemas.purchase_transaction import PurchaseTransactionPostBody 

class PurchaseTransaction(models.Model):
    _name = 'purchase.transaction'
    _inherit = ['purchase.transaction', 'api.resource']
    
    
    @api.model
    def _prepare_api_values(
        self,
        body: Optional[PurchaseTransactionPostBody] = None,
        vals: Optional[dict] = None
    ):
        vals = super()._prepare_api_values(body, vals)
        normalize_datetime_field(vals, 'date')
        map_relational_field(self.env, vals, 'partner_id', 'res.partner')
        map_relational_field(self.env, vals, 'operating_unit_id', 'operating.unit')
        map_relational_field(self.env, vals, 'delivery_method_id', 'ecocycle.delivery.method')
        map_relational_field(self.env, vals, 'delivery_address_id', 'res.partner')
        

        line_ids_payload = vals.pop('line_ids', [])
        vals['line_ids'] = []
        for line_payload in line_ids_payload:
            map_relational_field(self.env, line_payload, 'waste_category_id', 'waste.category')
            vals['line_ids'].append((0, 0, line_payload))

        return vals
    

class PurchaseTransactionItem(models.Model):
    _name = 'purchase.transaction.item'
    _inherit = ['purchase.transaction.item', 'api.resource']
