from odoo import api, fields, models, _
from odoo.exceptions import UserError
import random

class DailyCheckPoint(models.Model):
    _name = 'daily.check.point'
    _description = 'Daily Check Point'

    name = fields.Char(string="Label", required=True)
    sequence = fields.Integer(string="Sequence", required=True)
    point = fields.Float(string="Point", required=False)
    rendom_point_start = fields.Float(string="Random Point Start", required=False)
    rendom_point_end = fields.Float(string="Random Point End", required=False)
    is_random = fields.Boolean(string="Is Random")
    
    @api.constrains('is_random', 'rendom_point_start', 'rendom_point_end')
    def _check_random_point(self):
        if self.is_random:
            if self.rendom_point_end < self.rendom_point_start:
                raise UserError("End Point must be greater than Start Point")
    
    
    def get_point(self):
        if self.is_random:
            return round(
                random.uniform(self.rendom_point_start, self.rendom_point_end),
                2
            )
        
        return self.point or 0
    