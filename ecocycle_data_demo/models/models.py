# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class ecocycle_data_demo(models.Model):
#     _name = 'ecocycle_data_demo.ecocycle_data_demo'
#     _description = 'ecocycle_data_demo.ecocycle_data_demo'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

