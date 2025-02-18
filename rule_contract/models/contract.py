# File: models/contract.py
from odoo import models, fields, api

class CustomContract(models.Model):
    _name = 'custom.contract'
    _description = 'Hợp đồng'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    state = fields.Selection([
        ('draft', 'Bản nháp'),
        ('manager_approve', 'Chờ Quản lý duyệt'),
        ('director_approve', 'Chờ Giám đốc duyệt'),
        ('done', 'Đã duyệt')
    ], default='draft', tracking=True)

    # Trạng thái phê duyệt
    manager_approved_id = fields.Many2one('res.users', string="Người duyệt (QL)")
    director_approved_id = fields.Many2one('res.users', string="Người duyệt (GĐ)")

    # Phân quyền theo state
    def action_send_to_manager(self):
        self.write({'state': 'manager_approve'})

    def action_manager_approve(self):
        self.write({
            'state': 'director_approve',
            'manager_approved_id': self.env.user.id
        })

    def action_director_approve(self):
        self.write({
            'state': 'done',
            'director_approved_id': self.env.user.id
        })