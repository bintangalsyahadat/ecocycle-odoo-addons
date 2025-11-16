from odoo import api, fields, models

class EcoCyclePointHistory(models.Model):
    _name = 'ecocycle.point.history'
    _description = 'EcoCycle Point History'

    date = fields.Date(string="Date", required=True, default=fields.Date.context_today)
    partner_id = fields.Many2one(comodel_name="res.partner", string="Partner", required=True, ondelete="restrict", index=True)
    amount = fields.Float(string="Amount", required=False)