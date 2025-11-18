from odoo import api, fields, models

class SalesTransaction(models.Model):
    _name = 'sale.transaction'
    _inherit = ['sale.transaction', 'api.resource']
    

class SalesTransactionItem(models.Model):
    _name = 'sale.transaction.item'
    _inherit = ['sale.transaction.item', 'api.resource']
