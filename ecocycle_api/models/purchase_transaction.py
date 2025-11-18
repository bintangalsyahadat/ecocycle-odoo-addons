from odoo import api, fields, models

class PurchaseTransaction(models.Model):
    _name = 'purchase.transaction'
    _inherit = ['purchase.transaction', 'api.resource']
    

class PurchaseTransactionItem(models.Model):
    _name = 'purchase.transaction.item'
    _inherit = ['purchase.transaction.item', 'api.resource']
