# -*- coding: utf-8 -*-
# from odoo import http


# class EcocycleBase(http.Controller):
#     @http.route('/ecocycle_base/ecocycle_base', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/ecocycle_base/ecocycle_base/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('ecocycle_base.listing', {
#             'root': '/ecocycle_base/ecocycle_base',
#             'objects': http.request.env['ecocycle_base.ecocycle_base'].search([]),
#         })

#     @http.route('/ecocycle_base/ecocycle_base/objects/<model("ecocycle_base.ecocycle_base"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('ecocycle_base.object', {
#             'object': obj
#         })

