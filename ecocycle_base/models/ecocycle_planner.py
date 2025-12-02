# models/ecocycle_planner.py
from odoo import api, fields, models
from odoo.exceptions import ValidationError
import requests
import json
from datetime import datetime
import pytz


class EcoCyclePlanner(models.Model):
    _name = 'ecocycle.planner'
    _description = 'EcoCycle Planner'

    name = fields.Char(string="Name")
    date = fields.Date(string="Date", required=True,
                       default=fields.Date.context_today)
    partner_id = fields.Many2one(
        comodel_name="res.partner",
        string="Partner",
        required=True,
        ondelete="restrict",
        index=True,
    )
    point_rewarded = fields.Float(string="Point Rewarded")
    state = fields.Selection(
        selection=[
            ('pending', 'Pending'),
            ('done', 'Done'),
            ('expired', 'Expired'),
        ],
        string="Status",
        required=True,
        default='pending',
    )

    _sql_constraints = [
        (
            'unique_partner_date',
            'unique(partner_id, date)',
            'A planner for this partner on that date already exists.',
        ),
    ]

    def unlink(self):
        for rec in self:
            if rec.state != 'pending':
                raise ValidationError(
                    "Planner can only be deleted when status is 'Pending'.")
        return super().unlink()

    def action_send_whatsapp(self):
        """
        Send a WhatsApp text message via our own Node.js Baileys bot.
        This method will set record.state = 'done' on success.
        """
        params = self.env['ir.config_parameter'].sudo()
        portal_url = params.get_param("portal.url") or ""
        bot_endpoint = params.get_param('ecocycle.whatsapp.bot_endpoint')

        if not bot_endpoint:
            raise ValidationError("WhatsApp bot endpoint not configured.")

        for rec in self:
            if not rec.partner_id.phone:
                return False
                # raise ValidationError(
                #     f"Partner '{rec.partner_id.name}' has no phone number configured.")

            body_text = (
                f"Hello, {rec.partner_id.name}!\n\n"
                f"It’s time to recycle your waste!\n"
                f"Your EcoPlanner is scheduled for {rec.date}.\n\n"
                f"View details here:\n{portal_url}/ecoplanner"
            )

            payload = {
                "number": rec.partner_id.phone,
                "message": body_text,
            }

            response = requests.post(bot_endpoint, json=payload)
        return True

    def action_set_expired(self):
        """
        Set record status to 'expired' when date has passed and it is still pending.
        """
        for rec in self:
            rec.state = 'expired'
        return True

    @api.model
    def cron_send_whatsapp(self):
        tz = pytz.timezone('Asia/Jakarta')
        today = datetime.now(tz).date()

        domain = [
            ('state', '=', 'pending'),
            ('date', '=', today),
        ]
        records = self.search(domain)
        for rec in records:
            rec.action_send_whatsapp()

    @api.model
    def cron_expire_planners(self):
        """
        Cron job: Expire all pending planners whose date is older than today.
        """
        tz = pytz.timezone('Asia/Jakarta')
        today = datetime.now(tz).date()

        domain = [
            ('state', '=', 'pending'),
            ('date', '=', today),
        ]
        
        expired_recs = self.search(domain)
        expired_recs.action_set_expired()
        return True
