from odoo import api, fields, models


class WasteMove(models.Model):
    _name = 'waste.move'
    _description = 'Waste Move'

    date = fields.Datetime(string="Date", required=True, default=fields.Datetime.now)
    type = fields.Selection(string="Type", selection=[(
        'incoming', 'Incoming'), ('outgoing', 'Outgoing')], required=True)
    category_id = fields.Many2one(comodel_name="waste.category", string="Category", required=True, ondelete="restrict", index=True)
    operating_unit_id = fields.Many2one(comodel_name="operating.unit", string="Operating Unit", required=True, ondelete="restrict", index=True)
    quantity = fields.Float(string="Quantity", required=False)
    valid_qty = fields.Float(string="Valid QTY", required=False)
    state = fields.Selection(string="Status", selection=[('forecasted', 'Forecasted'), (
        'done', 'Done'), ('cancel', 'Cancelled')], required=True, default="forecasted")
    waste_picking_id = fields.Many2one(
        comodel_name="waste.picking", string="Waste Picking", required=False, ondelete="cascade", index=True)
    
    
    def action_done(self):
        for record in self:
            record.state = 'done'
            
    def action_cancel(self):
        for record in self:
            record.state = 'cancel'
