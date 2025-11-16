from odoo import api, fields, models

class ResPartner(models.Model):
    _inherit = 'res.partner'

    firebase_uuid = fields.Char(string="Firebase UUID", required=False)
    current_ou_id = fields.Many2one(comodel_name="operating.unit", string="Current Operating Unit", required=False, ondelete="restrict", index=True)
    coin_history_ids = fields.One2many(comodel_name="ecocycle.coin.history", inverse_name="partner_id", string="Coin History", required=False)
    point_history_ids = fields.One2many(comodel_name="ecocycle.point.history", inverse_name="partner_id", string="Point History", required=False)
    total_coin = fields.Float(string="Total Coin", required=False, compute="_compute_total_coin", store=True)
    total_point = fields.Float(string="Total Point", required=False, compute="_compute_total_point", store=True)

    @api.depends("coin_history_ids")
    def _compute_total_coin(self):
        for record in self:
            record.total_coin = sum(record.coin_history_ids.mapped("coin"))

    @api.depends("point_history_ids")
    def _compute_total_point(self):
        for record in self:
            record.total_point = sum(record.point_history_ids.mapped("point"))
    