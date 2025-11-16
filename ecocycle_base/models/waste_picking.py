from odoo import api, fields, models


class WastePicking(models.Model):
    _name = 'waste.picking'
    _description = 'Waste Picking'

    name = fields.Char(string="Number", required=False)
    partner_id = fields.Many2one(comodel_name="res.partner", string="Partner", required=True, ondelete="restrict", index=True)
    date = fields.Datetime(string="Date", required=True,
                           default=fields.Datetime.now)
    operating_unit_id = fields.Many2one(comodel_name="operating.unit", string="Operating Unit", required=True, ondelete="restrict", index=True)
    waste_move_ids = fields.One2many(comodel_name="waste.move", inverse_name="waste_picking_id", string="Waste Picking", required=False)
    delivery_method_id = fields.Many2one(comodel_name="ecocycle.delivery.method", string="Delivery Method", required=False, ondelete="restrict", index=True)
    state = fields.Selection(string="Status", selection=[
        ('draft', 'Draft'),
        ('confirm', 'Confirmed'),
        ('done', 'Done'),
        ('cancel', 'Cancelled'),
    ], required=True, default="draft")
    
    @api.model
    def create(self, values):
        res = super(WastePicking, self).create(values)
        res.action_confirm()
        return res

    def action_confirm(self):
        for rec in self:
            if rec.state == 'draft':
                rec.state = 'confirm'
                
                if not rec.name:
                    if rec.purchase_transaction_id:
                        rec.name = self.env['ir.sequence'].next_by_code(
                            'waste.picking.in') or False
                    else:
                        rec.name = self.env['ir.sequence'].next_by_code(
                            'waste.picking.out') or False

    def action_done(self):
        for rec in self:
            if rec.state == 'confirm':
                rec.state = 'done'
                rec.waste_move_ids.action_done()
                
    def action_cancel(self):
        for rec in self:
            if rec.state in ['draft', 'confirm']:
                rec.state = 'cancel'
                rec.waste_move_ids.action_cancel()

