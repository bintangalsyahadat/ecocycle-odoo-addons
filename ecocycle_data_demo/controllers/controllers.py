# -*- coding: utf-8 -*-
# from odoo import http


# class EcocycleDataDemo(http.Controller):
#     @http.route('/ecocycle_data_demo/ecocycle_data_demo', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/ecocycle_data_demo/ecocycle_data_demo/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('ecocycle_data_demo.listing', {
#             'root': '/ecocycle_data_demo/ecocycle_data_demo',
#             'objects': http.request.env['ecocycle_data_demo.ecocycle_data_demo'].search([]),
#         })

#     @http.route('/ecocycle_data_demo/ecocycle_data_demo/objects/<model("ecocycle_data_demo.ecocycle_data_demo"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('ecocycle_data_demo.object', {
#             'object': obj
#         })

