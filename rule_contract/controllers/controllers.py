# -*- coding: utf-8 -*-
# from odoo import http


# class RuleContract(http.Controller):
#     @http.route('/rule_contract/rule_contract', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/rule_contract/rule_contract/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('rule_contract.listing', {
#             'root': '/rule_contract/rule_contract',
#             'objects': http.request.env['rule_contract.rule_contract'].search([]),
#         })

#     @http.route('/rule_contract/rule_contract/objects/<model("rule_contract.rule_contract"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('rule_contract.object', {
#             'object': obj
#         })
