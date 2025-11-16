from odoo import api, fields, models

class PaymentTransaction(models.Model):
    _name = 'payment.transaction'
    _description = 'Payment Transaction'

    name = fields.Char(string="Name", required=False)
    memo = fields.Char(string="Memo", required=False)
    date = fields.Date(string="Date", required=True, default=fields.Date.context_today)
    partner_id = fields.Many2one(comodel_name="res.partner", string="Partner", required=True, ondelete="restrict", index=True)
    amount = fields.Float(string="Amount", required=False)
    payment_method_id = fields.Many2one(comodel_name="ecocycle.payment.method", string="Payment Method", required=True, ondelete="restrict", index=True)
    operating_unit_id = fields.Many2one(comodel_name="operating.unit", string="Operating Unit", required=True, ondelete="restrict", index=True)
    state = fields.Selection(string="Status", selection=[('draft', 'Draft'), ('paid', 'Paid')], required=True, default="draft")
    type = fields.Selection(string="Type", selection=[('incoming', 'Incoming'), ('outgoing', 'Outgoing')], required=True)
    sale_transaction_id = fields.Many2one(comodel_name="sale.transaction", string="Sale Transaction", required=False, ondelete="restrict", index=True)
    purchase_transaction_id = fields.Many2one(comodel_name="purchase.transaction", string="Purchase Transaction", required=False, ondelete="restrict", index=True)
    
    def action_paid(self):
        self.write({'state': 'paid'})
        if self.sale_transaction_id:
            self.sale_transaction_id.action_payment()
            