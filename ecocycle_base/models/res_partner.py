from odoo import api, fields, models

class ResPartner(models.Model):
    _inherit = 'res.partner'

    firebase_uuid = fields.Char(string="Firebase UUID", required=False)
    current_ou_id = fields.Many2one(comodel_name="operating.unit", string="Current Operating Unit", required=False, ondelete="restrict", index=True)
    