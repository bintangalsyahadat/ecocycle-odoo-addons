from odoo import api, fields, models

class EcoCyclePlanner(models.Model):
    _inherit = 'ecocycle.planner'

    
    purchase_transaction_id = fields.Many2one(
        comodel_name="purchase.transaction",
        string="Purchase Transaction",
        ondelete="restrict",
        index=True,
    )