from odoo import api, fields, models

class WastePicking(models.Model):
    _name = 'waste.picking'
    _inherit = ['waste.picking', 'api.resource']
