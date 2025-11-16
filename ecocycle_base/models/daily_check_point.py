from odoo import api, fields, models

class DailyCheckPoint(models.Model):
    _name = 'daily.check.point'
    _description = 'Daily Check Point'

    sequence = fields.Integer(string="Sequence", required=True)
    point = fields.Float(string="Point", required=True)
    is_final = fields.Boolean(string="Is Final")
    