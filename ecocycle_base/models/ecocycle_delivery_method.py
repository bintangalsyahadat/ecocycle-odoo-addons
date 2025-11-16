from odoo import api, fields, models

class DeliveryMethod(models.Model):
    _name = 'ecocycle.delivery.method'
    _description = 'Delivery Method'
    
    name = fields.Char(string="Name", required=True)
    description = fields.Char(string="Description", required=False)
    type = fields.Selection(string="Type", selection=[('sale', 'Sale'), ('purchase', 'Purchase')], required=True)
    is_self_service = fields.Boolean(string="Self Service", required=False, default=False)