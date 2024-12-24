# -*- coding: utf-8 -*-
# from odoo import http


# class ContractDuration(http.Controller):
#     @http.route('/contract_duration/contract_duration', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/contract_duration/contract_duration/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('contract_duration.listing', {
#             'root': '/contract_duration/contract_duration',
#             'objects': http.request.env['contract_duration.contract_duration'].search([]),
#         })

#     @http.route('/contract_duration/contract_duration/objects/<model("contract_duration.contract_duration"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('contract_duration.object', {
#             'object': obj
#         })
