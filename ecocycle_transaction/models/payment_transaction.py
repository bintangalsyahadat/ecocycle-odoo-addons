from odoo import api, fields, models
import requests
import json
import logging
from datetime import datetime

_logger = logging.getLogger(__name__)

class PaymentTransaction(models.Model):
    _name = 'payment.transaction'
    _description = 'Payment Transaction'

    name = fields.Char(string="Name", required=False)
    memo = fields.Char(string="Memo", required=False)
    date = fields.Date(string="Date", required=True, default=fields.Date.context_today)
    payment_date = fields.Datetime(string="Payment Date", required=False)
    partner_id = fields.Many2one(
        comodel_name="res.partner", string="Partner", required=True, ondelete="restrict", index=True)
    amount = fields.Float(string="Amount", required=False)
    payment_method_id = fields.Many2one(comodel_name="ecocycle.payment.method",
                                        string="Payment Method", required=True, ondelete="restrict", index=True)
    operating_unit_id = fields.Many2one(
        comodel_name="operating.unit", string="Operating Unit", required=True, ondelete="restrict", index=True)
    state = fields.Selection([
        ("draft", "Draft"),
        ("pending", "Pending"),
        ("paid", "Paid"),
        ("failed", "Failed"),
        ("expired", "Expired")
    ], default="draft")
    type = fields.Selection(string="Type", selection=[(
        'incoming', 'Incoming'), ('outgoing', 'Outgoing')], required=True)
    sale_transaction_id = fields.Many2one(
        comodel_name="sale.transaction", string="Sale Transaction", required=False, ondelete="restrict", index=True)
    purchase_transaction_id = fields.Many2one(
        comodel_name="purchase.transaction", string="Purchase Transaction", required=False, ondelete="restrict", index=True)
    xendit_invoice_id = fields.Char(string="Xendit Invoice ID", required=False)
    xendit_checkout_url = fields.Char(
        string="Xendit Checkout URL", required=False)
    xendit_expired_date = fields.Datetime(
        string="Xendit Expired Date", required=False)

    def action_paid(self):
        self.write({'state': 'paid'})
        if self.sale_transaction_id:
            self.sale_transaction_id.action_payment()

    def action_create_xendit_invoice(self):
        portal_url = self.env['ir.config_parameter'].sudo(
        ).get_param("portal.url")
        secret_key = self.env['ir.config_parameter'].sudo(
        ).get_param("xendit.secret_key")
        type = "buy" if self.type == "incoming" else "sell"
        transaction_name = self.sale_transaction_id.name if self.sale_transaction_id else self.purchase_transaction_id.name

        payload = {
            "external_id": transaction_name + "-" + str(self.id),
            "amount": self.amount or 0,
            "currency": "IDR",
            "payer_email": self.partner_id.email,
            "payment_methods": [self.payment_method_id.code],
            "success_redirect_url": "%s/transaction/%s/%s" % (portal_url, type, transaction_name),
            "failure_redirect_url": "%s/transaction/%s/%s" % (portal_url, type, transaction_name),
        }

        response = requests.post(
            "https://api.xendit.co/v2/invoices",
            auth=(secret_key, ""),
            json=payload,
            headers={"Content-Type": "application/json"}
        )

        res = response.json()
        if response.status_code not in [200, 201]:
            raise Exception(f"Xendit Error: {res}")

        expiry_raw = res.get("expiry_date")
        expiry_date = None

        if expiry_raw:
            try:
                iso_fixed = expiry_raw.replace("Z", "+00:00")
                dt = datetime.fromisoformat(iso_fixed)
                expiry_date = fields.Datetime.to_string(dt)
            except Exception as e:
                _logger.error("Failed parsing expiry date: %s", e)

        self.sudo().write({
            "xendit_invoice_id": res.get("id"),
            "xendit_checkout_url": res.get("invoice_url"),
            "xendit_expired_date": expiry_date,
            "state": "pending",
        })

        return res

    def action_update_xendit_state(self, state):
        state_map = {
            "PAID": "paid",
            "EXPIRED": "expired",
            "FAILED": "failed",
            "PENDING": "pending",
        }

        self.sudo().write({
            "payment_date": fields.Datetime.now(),
            "state": state_map.get(state, "pending")
        })
        
        if self.sudo().sale_transaction_id:
            self.sudo().sale_transaction_id.action_payment()
