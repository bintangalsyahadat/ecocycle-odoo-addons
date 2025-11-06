from odoo import api, fields, models


class WasteCategoryPricelist(models.Model):
    _name = 'waste.category.pricelist'
    _description = 'Waste Category Pricelist'

    name = fields.Char(string="Name", compute="_compute_name", required=False)
    operating_unit_id = fields.Many2one(
        comodel_name="operating.unit", string="Operating Unit", required=True, ondelete="restrict", index=True)
    type = fields.Selection(string="Type", selection=[(
        'sale', 'Selling Price'), ('purchase', 'Purchase Price')], required=False)
    category_id = fields.Many2one(comodel_name="waste.category",
                                  string="Category", required=True, ondelete="restrict", index=True)
    price = fields.Float(string="Price", required=True)

    _sql_constraints = [
        (
            'unique_ou_category_type',
            'unique(operating_unit_id, category_id, type)',
            'Combination of Operating Unit, Category, and Type must be unique!'
        ),
    ]

    @api.depends('operating_unit_id', 'category_id')
    def _compute_name(self):
        for record in self:
            record.name = f"{record.operating_unit_id.name} - {record.category_id.name}"
