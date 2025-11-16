from odoo import api, fields, models


class WastePicking(models.Model):
    _inherit = 'waste.picking'

    purchase_transaction_id = fields.Many2one(
        comodel_name="purchase.transaction", string="Purchase Transaction", required=False, ondelete="restrict", index=True)
    sale_transaction_id = fields.Many2one(
        comodel_name="sale.transaction", string="Purchase Transaction", required=False, ondelete="restrict", index=True)

    def action_done(self):
        super(WastePicking, self).action_done()
        for rec in self:
            if rec.sale_transaction_id:
                rec.purchase_transaction_id.action_done()
            if rec.purchase_transaction_id:
                rec.sale_transaction_id.action_done()


class WasteMove(models.Model):
    _inherit = 'waste.move'

    waste_picking_id = fields.Many2one(
        comodel_name="waste.picking", string="Waste Picking", required=False, ondelete="restrict", index=True)
    purchase_transaction_item_id = fields.Many2one(
        comodel_name="purchase.transaction.item", string="Purchase Transaction Item", required=False, ondelete="restrict", index=True)
    sale_transaction_item_id = fields.Many2one(
        comodel_name="sale.transaction.item", string="Sale Transaction Item", required=False, ondelete="restrict", index=True)
    
    
