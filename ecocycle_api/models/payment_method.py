from odoo import api, fields, models

class PaymentMethod(models.Model):
    _name = 'ecocycle.payment.method'
    _inherit = ['ecocycle.payment.method', 'api.resource']
