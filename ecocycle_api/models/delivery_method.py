from odoo import api, fields, models

class DeliveryMethod(models.Model):
    _name = 'ecocycle.delivery.method'
    _inherit = ['ecocycle.delivery.method', 'api.resource']
