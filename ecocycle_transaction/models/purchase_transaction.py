from odoo import api, fields, models, _


class PurchaseTransaction(models.Model):
    _name = 'purchase.transaction'
    _description = 'Purchase Transaction'
    _order= 'date desc, id desc'

    name = fields.Char(string="Transaction Number", required=False, default="Draft", copy=False)
    date = fields.Datetime(string="Date", required=True, default=fields.Datetime.now)
    scheduled_date = fields.Datetime(string="Scheduled Date", required=False)
    partner_id = fields.Many2one(
        comodel_name="res.partner", string="Partner", required=True, ondelete="restrict", index=True)
    operating_unit_id = fields.Many2one(
        comodel_name="operating.unit", string="Operating Unit", required=True, ondelete="restrict", index=True)
    estimate_total_amount = fields.Float(
        string="Total Amount", compute="_compute_total_amount", store=True)
    total_amount = fields.Float(
        string="Total Amount", compute="_compute_total_amount", store=True)
    line_ids = fields.One2many(comodel_name="purchase.transaction.item",
                               inverse_name="purchase_transaction_id", string="Lines", required=False)
    picking_ids = fields.One2many(comodel_name="waste.picking", inverse_name="purchase_transaction_id", string="Pickings", required=False)
    delivery_method_id = fields.Many2one(comodel_name="ecocycle.delivery.method", string="Delivery Method", required=True, ondelete="restrict", index=True)
    delivery_address_id = fields.Many2one(comodel_name="res.partner", string="Delivery Address", required=False, ondelete="restrict", index=True)
    is_self_service = fields.Boolean(related='delivery_method_id.is_self_service', store=True, readonly=True)
    planner_id = fields.Many2one(comodel_name="ecocycle.planner", string="Planner", required=False, ondelete="restrict", index=True)
    state = fields.Selection(string="Status", selection=[
        ('draft', 'Draft'),
        ('waiting_approval', 'Waiting Approval'),
        ('waiting_process', 'Waiting Process'),
        ('purchased', 'Purchased'),
        ('cancel', 'Cancelled'),
        ('reject', 'Rejected')
    ], required=True, default="draft")
    note = fields.Char(string="Note", required=False)
    
    @api.depends('line_ids', 'line_ids.estimate_total_price', 'line_ids.total_price')
    def _compute_total_amount(self):
        for record in self:
            record.estimate_total_amount = sum(record.line_ids.mapped('estimate_total_price'))
            record.total_amount = sum(record.line_ids.mapped('total_price'))
    
    def action_confirm(self):
        for rec in self:
            if rec.state == 'draft':
                rec.name = self.env['ir.sequence'].next_by_code('purchase.transaction') or False
                
                planner = self.env['ecocycle.planner'].search([('date', '=', rec.date), ('state', '=', 'pending')], limit=1)
                if planner:
                    rec.planner_id = planner
                
                if rec.delivery_method_id.is_self_service:
                    rec.state = 'waiting_process'
                    rec._create_picking()
                else:
                    rec.state = 'waiting_approval'
                
    def action_approve(self):
        for rec in self:
            if rec.state == 'waiting_approval':
                rec.state = 'waiting_process'
                rec._create_picking()
                
    def action_cancel(self):
        for rec in self:
            if rec.state in ['draft', 'waiting_approval', 'waiting_process']:
                rec.state = 'cancel'
    
    def action_reject(self):
        for rec in self:
            if rec.state in ['waiting_approval']:
                rec.state = 'reject'
                
    def action_done(self):
        for rec in self:
            if rec.state == 'waiting_process':
                rec.state = 'purchased'
                rec.update_partner_reward()
                
    def update_partner_reward(self):
        for rec in self:
            if rec.state == 'purchased':
                coin = total_amount
                point = floor(total_amount / 1000)
                
                if rec.planner_id:
                    rec.planner_id.point_rewarded = point
                    point *= 2
                    
                self.partner_id.update_coin(coin)
                self.partner_id.update_point(point)
                
                
    def _create_picking(self):
        self.ensure_one()
        vals = self._prepare_waste_picking()
        
        waste_move_vals = []
        for line in self.line_ids:
            waste_move_vals.append((0, 0, line._preapre_waste_move()))
            
        vals['waste_move_ids'] = waste_move_vals
        return self.env['waste.picking'].create(vals)
                
    def _prepare_waste_picking(self):
        return {
            'purchase_transaction_id': self.id,
            'operating_unit_id': self.operating_unit_id.id,
            'partner_id': self.partner_id.id
        }
        
    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        self.operating_unit_id = self.partner_id.current_ou_id
        
    @api.onchange('delivery_method_id')
    def _onchange_delivery_method_id(self):
        if self.delivery_method_id and not self.delivery_method_id.is_self_service:
            if not self.delivery_address_id:
                self.delivery_address_id = self.partner_id
        else:
            self.delivery_address_id = False
        
    def action_open_pickings(self):
        self.ensure_one()
        pickings = self.picking_ids

        action = {
            "type": "ir.actions.act_window",
            "res_model": "waste.picking",
            "view_mode": "tree,form",
            "domain": [("id", "in", pickings.ids)],
            "context": {"default_purchase_transaction_id": self.id},
        }

        if len(pickings) == 1:
            action.update({
                "view_mode": "form",
                "res_id": pickings.id,
                "domain": False,
            })
        return action
    
    def action_process(self):
        self.ensure_one()
        action = {
            'name': _("Process"),
            "type": "ir.actions.act_window",
            "res_model": "waste.picking",
            "view_mode": "form",
            "view_id": self.env.ref("ecocycle_transaction.form_picking_process").id,
            "res_id": self.picking_ids.id,
            "target": "new"
        }
        
        return action
        


class PurchaseTransactionItem(models.Model):
    _name = 'purchase.transaction.item'
    _description = 'Purchase Transaction Item'

    purchase_transaction_id = fields.Many2one(
        comodel_name="purchase.transaction", string="Purchase", required=False, ondelete="cascade", index=True)
    waste_category_id = fields.Many2one(
        comodel_name="waste.category", string="Waste Category", required=True, ondelete="restrict", index=True)
    quantity = fields.Float(string="Quantity", required=True, default=1)
    unit_price = fields.Float(string="Unit Price", required=False, compute="compute_price", store=True)
    estimate_total_price = fields.Float(
        string="Estimate Total Price", compute="_compute_total", store=True)
    total_price = fields.Float(
        string="Total Price", compute="_compute_total", store=True)
    move_ids = fields.One2many(comodel_name="waste.move", inverse_name="purchase_transaction_item_id", string="Moves", required=False)
    valid_qty = fields.Float(string="Valid QTY", compute="_compute_qty", store=True)
    operating_unit_id = fields.Many2one(related='purchase_transaction_id.operating_unit_id', store=True)
    
    @api.depends('move_ids', 'move_ids.valid_qty', 'move_ids.state')
    def _compute_qty(self):
        for record in self:
            moves = record.move_ids.filtered(lambda move: move.state == 'done')
            record.valid_qty = sum(moves.mapped('valid_qty'))

    @api.depends('quantity', 'unit_price', 'valid_qty')
    def _compute_total(self):
        for record in self:
            record.estimate_total_price = record.quantity * record.unit_price
            record.total_price = record.valid_qty * record.unit_price
            
    @api.depends('waste_category_id')
    def compute_price(self):
        for rec in self:
            rec.unit_price = rec.waste_category_id.purchase_price
            
    def _preapre_waste_move(self):
        return {
            'purchase_transaction_item_id': self.id,
            'operating_unit_id': self.purchase_transaction_id.operating_unit_id.id,
            'category_id': self.waste_category_id.id,
            'quantity': self.quantity,
            'type': 'incoming'
        }
