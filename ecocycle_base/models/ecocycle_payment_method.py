from odoo import api, fields, models


class PaymentMethod(models.Model):
    _name = 'ecocycle.payment.method'
    _description = 'Payment Method'

    name = fields.Char(string="Name", required=True)
    code = fields.Char(string="Code", required=True)
    description = fields.Char(string="Description", required=False)
