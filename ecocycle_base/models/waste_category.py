from odoo import api, fields, models


class WasteCategory(models.Model):
    _name = 'waste.category'
    _description = 'Waste Category'

    name = fields.Char(string="Name", required=True)
    description = fields.Char(string="Description", required=False)
    image = fields.Binary(string="Image")
    price = fields.Float(string="Price", required=True)
    pricelist_ids = fields.One2many(comodel_name="waste.category.pricelist",
                                    inverse_name="category_id", string="Pricelist", required=False)
    move_ids = fields.One2many(comodel_name="waste.move", inverse_name="category_id", string="Moves", required=False)
    stock_move_in = fields.Float(string="Stock Move Incoming", compute="_compute_moves", store=True)
    stock_move_out = fields.Float(string="Stock Move Outgoing", compute="_compute_moves", store=True)
    stock_forecasted = fields.Float(string="Stock Forecasted", compute="_compute_moves", store=True)
    
    @api.depends('move_ids')
    def _compute_moves(self):
        for rec in self:
            move_in = 0
            move_out = 0
            quants_forecasted = 0
            
            for move in rec.move_ids:
                if move.operating_unit_id.id in self.env.user.operating_unit_ids.ids:
                    if move.state == 'done':
                        if move.type == 'incoming':
                            moves_done_in += move.quantity
                        if move.type == 'outgoing':
                            move_out += move.quantity
                    if move.state == 'forecasted':
                        if move.type == 'incoming':
                            quants_forecasted += move.quantity
                        if move.type == 'outgoing':
                            quants_forecasted -= move.quantity
                    
            rec.stock_move_in = move_in
            rec.stock_move_out = move_out
            rec.stock_forecasted = (
                move_in - move_out) + quants_forecasted

    def get_price(self, type, operating_unit):
        price = 0

        price_from_pricelist = self.pricelist_ids.filtered(
            lambda x: x.operating_unit_id == operating_unit and x.type == type
        )
        
        if price_from_pricelist:
            price = price_from_pricelist[0].price
            
        return price
    
    def get_stock(self, operating_unit):
        move_in = 0
        move_out = 0
        quants_forecasted = 0
        
        for move in self.move_ids:
            if move.operating_unit_id.id == operating_unit.id:
                if move.state == 'done':
                    if move.type == 'incoming':
                        moves_done_in += move.quantity
                    if move.type == 'outgoing':
                        move_out += move.quantity
                if move.state == 'forecasted':
                    if move.type == 'incoming':
                        quants_forecasted += move.quantity
                    if move.type == 'outgoing':
                        quants_forecasted -= move.quantity
        
        return {
            'qty_forecasted': (move_in - move_out) + quants_forecasted,
            'operating_unit_id': operating_unit.id
        }
