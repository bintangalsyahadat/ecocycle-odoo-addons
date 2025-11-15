from odoo import api, fields, models

class OperatingUnit(models.Model):
    _name = 'operating.unit'
    _inherit = ['operating.unit', 'api.resource']
