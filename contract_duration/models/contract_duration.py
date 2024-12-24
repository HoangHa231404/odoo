# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import logging
_logger = logging.getLogger(__name__)


class ContractDuration(models.Model):
    _inherit = 'sale.order'
   
    x_contract_duration = fields.Integer(
        string = "Contract Duration",
        required = True,
        default=0)
    x_contract_time_type = fields.Selection(
        [
            ('days','Ngày'),
            ('weeks','Tuần'),
            ('months','Tháng'),
            ('years','Năm')
        ],
        required=True,default='days',
        comodel_name='contract.time.type',
        string="Contract Time Type")
    contract_note = fields.Text(string="Ghi chú hợp đồng", compute="_compute_contract_note")

    @api.depends('x_contract_duration', 'x_contract_time_type')
    def _compute_contract_note(self):
        for order in self:
            if order.x_contract_duration and order.x_contract_time_type:
                time_type_translations = { 'days': 'ngày', 'weeks': 'tuần', 'months': 'tháng', 'years': 'năm' } 
                translated_time_type = time_type_translations.get(order.x_contract_time_type, order.x_contract_time_type)
                order.contract_note = f"Thời gian hợp đồng: {order.x_contract_duration} {translated_time_type}"
            else:
                order.contract_note = ''


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.model
    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()

        self._create_invoices()

        return res

    