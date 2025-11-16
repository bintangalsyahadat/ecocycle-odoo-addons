# -*- coding: utf-8 -*-
# from odoo import http


# class EcocycleTransaction(http.Controller):
#     @http.route('/ecocycle_transaction/ecocycle_transaction', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/ecocycle_transaction/ecocycle_transaction/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('ecocycle_transaction.listing', {
#             'root': '/ecocycle_transaction/ecocycle_transaction',
#             'objects': http.request.env['ecocycle_transaction.ecocycle_transaction'].search([]),
#         })

#     @http.route('/ecocycle_transaction/ecocycle_transaction/objects/<model("ecocycle_transaction.ecocycle_transaction"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('ecocycle_transaction.object', {
#             'object': obj
#         })

