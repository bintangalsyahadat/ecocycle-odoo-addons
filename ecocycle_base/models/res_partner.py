from odoo import api, fields, models

class ResPartner(models.Model):
    _inherit = 'res.partner'

    firebase_uuid = fields.Char(string="Firebase UUID", required=False)