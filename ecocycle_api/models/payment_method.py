from odoo import api, fields, models

class PaymentMethod(models.Model):
    _name = 'ecocycle.payment.method'
    _inherit = ['ecocycle.payment.method', 'api.resource']
    
    
class PaymentTransaction(models.Model):
    _name = 'payment.transaction'
    _inherit = ['payment.transaction', 'api.resource']
