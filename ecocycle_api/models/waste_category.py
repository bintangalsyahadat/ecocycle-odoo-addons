from odoo import api, fields, models

class WasteCategory(models.Model):
    _name = 'waste.category'
    _inherit = ['waste.category', 'api.resource']
