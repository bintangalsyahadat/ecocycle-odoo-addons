# -*- coding: utf-8 -*-
# from odoo import http


# class EcocycleApi(http.Controller):
#     @http.route('/ecocycle_api/ecocycle_api', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/ecocycle_api/ecocycle_api/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('ecocycle_api.listing', {
#             'root': '/ecocycle_api/ecocycle_api',
#             'objects': http.request.env['ecocycle_api.ecocycle_api'].search([]),
#         })

#     @http.route('/ecocycle_api/ecocycle_api/objects/<model("ecocycle_api.ecocycle_api"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('ecocycle_api.object', {
#             'object': obj
#         })

