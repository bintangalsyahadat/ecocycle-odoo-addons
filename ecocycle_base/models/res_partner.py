from odoo import api, fields, models, _

class ResPartner(models.Model):
    _inherit = 'res.partner'

    firebase_uuid = fields.Char(string="Firebase UUID", required=False)
    current_ou_id = fields.Many2one(comodel_name="operating.unit", string="Current Operating Unit", required=False, ondelete="restrict", index=True)
    coin_history_ids = fields.One2many(comodel_name="ecocycle.coin.history", inverse_name="partner_id", string="Coin History", required=False)
    point_history_ids = fields.One2many(comodel_name="ecocycle.point.history", inverse_name="partner_id", string="Point History", required=False)
    total_coin = fields.Float(string="Total Coin", required=False, compute="_compute_total_coin", store=True)
    total_point = fields.Float(string="Total Point", required=False, compute="_compute_total_point", store=True)
    is_already_daily_checkin = fields.Boolean(string="Is Already Daily Checkin", compute="compute_is_already_daily_checkin", store=True)
    last_daily_check_at = fields.Date(string="Last Check-In At", required=False)
    last_daily_check_on = fields.Integer(string="Last Check-In On", required=False, default=0)
    ecoplanner_ids = fields.One2many(comodel_name="ecocycle.planner", inverse_name="partner_id", string="EcoPlanner", required=False)

    @api.depends("coin_history_ids")
    def _compute_total_coin(self):
        for record in self:
            record.total_coin = sum(record.coin_history_ids.mapped("amount"))

    @api.depends("point_history_ids")
    def _compute_total_point(self):
        for record in self:
            record.total_point = sum(record.point_history_ids.mapped("amount"))
            
    @api.depends("last_daily_check_at")
    def compute_is_already_daily_checkin(self):
        for record in self:
            if not record.last_daily_check_at:
                record.is_already_daily_checkin = False
            elif record.last_daily_check_at != fields.Date.today():
                record.is_already_daily_checkin = False
            else:
                record.is_already_daily_checkin = True
                
    def action_daily_check(self):
        self.ensure_one()
        if not self.is_already_daily_checkin:
            daily_check_point = self.env["daily.check.point"].search([])
            
            if self.last_daily_check_on == max(daily_check_point.mapped("sequence")):
                self.last_daily_check_on = 0
            
            daily_check_point = daily_check_point.filtered(lambda x: x.sequence == self.last_daily_check_on + 1)
            if daily_check_point:
                self.last_daily_check_at = fields.Date.today()
                self.last_daily_check_on = daily_check_point.sequence
                
                self.env['ecocycle.point.history'].create({
                    "partner_id": self.id,
                    "date": fields.Date.today(),
                    "amount": daily_check_point.get_point(),
                })
                
                return True
        return False
    
    def action_open_planner(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _("EcoPlanner"),
            'res_model': 'ecocycle.planner',
            'view_mode': 'list',
            'domain': [('partner_id', '=', self.id)],
            'context': {'default_partner_id': self.id},
            'target': 'current',
        }