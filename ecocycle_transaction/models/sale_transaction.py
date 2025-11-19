from odoo import api, fields, models, _


class SaleTransaction(models.Model):
    _name = 'sale.transaction'
    _description = 'Sale Transaction'
    _order = 'date desc, id desc'

    name = fields.Char(string="Transaction Number", required=False, default="Draft", copy=False)
    date = fields.Datetime(string="Date", required=True, default=fields.Datetime.now)
    partner_id = fields.Many2one(
        comodel_name="res.partner", string="Partner", required=True, ondelete="restrict", index=True)
    operating_unit_id = fields.Many2one(
        comodel_name="operating.unit", string="Operating Unit", required=True, ondelete="restrict", index=True)
    total_amount = fields.Float(
        string="Total Amount", compute="_compute_total_amount", store=True)
    line_ids = fields.One2many(comodel_name="sale.transaction.item",
                               inverse_name="sale_transaction_id", string="Lines", required=False)
    picking_ids = fields.One2many(comodel_name="waste.picking", inverse_name="sale_transaction_id", string="Pickings", required=False)
    delivery_method_id = fields.Many2one(comodel_name="ecocycle.delivery.method", string="Delivery Method", required=True, ondelete="restrict", index=True)
    delivery_address_id = fields.Many2one(comodel_name="res.partner", string="Delivery Address", required=False, ondelete="restrict", index=True)
    is_self_service = fields.Boolean(related='delivery_method_id.is_self_service', store=True, readonly=True)
    payment_method_id = fields.Many2one(comodel_name="ecocycle.payment.method", string="Payment Method", required=True, ondelete="restrict", index=True)
    payment_ids = fields.One2many(comodel_name="payment.transaction", inverse_name="sale_transaction_id", string="Payments", required=False)
    state = fields.Selection(string="Status", selection=[
        ('draft', 'Draft'),
        ('waiting_payment', 'Waiting Payment'),
        ('waiting_process', 'Waiting Process'),
        ('sale', 'Sale Order'),
        ('cancel', 'Cancelled')
    ], required=True, default="draft")
    note = fields.Char(string="Note", required=False)
    
    @api.depends('line_ids', 'line_ids.total_price')
    def _compute_total_amount(self):
        for record in self:
            record.total_amount = sum(record.line_ids.mapped('total_price'))
    
    def action_confirm(self):
        for rec in self:
            if rec.state == 'draft':
                rec.name = self.env['ir.sequence'].next_by_code('sale.transaction') or False
                payment = rec._create_payment()
                if payment:
                    rec.state = 'waiting_payment'
                
    def action_payment(self):
        for rec in self:
            if rec.state == 'waiting_payment':
                rec.state = 'waiting_process'
                rec._create_picking()
                
    def action_cancel(self):
        for rec in self:
            if rec.state in ['draft', 'waiting_payment']:
                rec.state = 'cancel'
                
    def action_done(self):
        for rec in self:
            if rec.state == 'waiting_process':
                rec.state = 'sale'
                
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
            'sale_transaction_id': self.id,
            'operating_unit_id': self.operating_unit_id.id,
            'partner_id': self.delivery_address_id.id if self.delivery_address_id else self.partner_id.id
        }
        
    def _create_payment(self):
        self.ensure_one()
        return self.env['payment.transaction'].create(self._prepare_payment_values())
        
    def _prepare_payment_values(self):
        return {
            'memo': "Payment for sale transaction " + self.name,
            'partner_id': self.partner_id.id,
            'payment_method_id': self.payment_method_id.id,
            'amount': self.total_amount,
            'operating_unit_id': self.operating_unit_id.id,
            'type': 'incoming',
            'sale_transaction_id': self.id
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
            "context": {"default_sale_transaction_id": self.id},
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
        


class SaleTransactionItem(models.Model):
    _name = 'sale.transaction.item'
    _description = 'Sale Transaction Item'

    sale_transaction_id = fields.Many2one(
        comodel_name="sale.transaction", string="Sale", required=False, ondelete="cascade", index=True)
    waste_category_id = fields.Many2one(
        comodel_name="waste.category", string="Waste Category", required=True, ondelete="restrict", index=True)
    quantity = fields.Float(string="Quantity", required=True, default=1)
    unit_price = fields.Float(string="Unit Price", required=False, compute="compute_price", store=True)
    total_price = fields.Float(
        string="Total Price", compute="_compute_total", store=True)
    move_ids = fields.One2many(comodel_name="waste.move", inverse_name="sale_transaction_item_id", string="Moves", required=False)
    operating_unit_id = fields.Many2one(related='sale_transaction_id.operating_unit_id', store=True)

    @api.depends('quantity', 'unit_price')
    def _compute_total(self):
        for record in self:
            record.total_price = record.quantity * record.unit_price
            
    @api.depends('waste_category_id')
    def compute_price(self):
        for rec in self:
            rec.unit_price = rec.waste_category_id.sales_price
            
    def _preapre_waste_move(self):
        return {
            'sale_transaction_item_id': self.id,
            'operating_unit_id': self.sale_transaction_id.operating_unit_id.id,
            'category_id': self.waste_category_id.id,
            'quantity': self.quantity,
            'type': 'incoming'
        }
