from odoo import api, fields, models

class DailyCheckPoint(models.Model):
    _name = 'daily.check.point'
    _inherit = ['daily.check.point', 'api.resource']
