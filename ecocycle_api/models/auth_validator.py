from odoo import api, fields, models


class AuthJWTValidator(models.Model):
    _inherit = 'auth.jwt.validator'

    def _get_partner_id(self, payload):
        if not self.partner_id_strategy:
            return self.static_user_id.partner_id.id
        return super(AuthJWTValidator, self)._get_partner_id(payload)
