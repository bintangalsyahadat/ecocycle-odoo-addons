from odoo import api, fields, models

class PaymentMethod(models.Model):
    _name = 'payment.method'
    _description = 'Payment Method'

    name = fields.Char(string="Name", required=True)