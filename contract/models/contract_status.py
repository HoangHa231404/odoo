from odoo import models, fields, api, exceptions

class Contract(models.Model):
    _inherit = 'contract.model'

    STATE_SELECTION = [
            ('draft', 'Nháp'),
            ('waiting_manager', 'Chờ Quản lý phê duyệt'),
            ('waiting_director', 'Chờ Giám đốc phê duyệt'),
            ('approved', 'Đã phê duyệt')
        ]

    state = fields.Selection(
        selection=STATE_SELECTION,
        string='Trạng thái',
        default='draft',
        track_visibility='onchange',
    )

    manager_approved = fields.Boolean(string="Quản lý phê duyệt")
    director_approved = fields.Boolean(string="Giám đốc phê duyệt")
    current_approver_id = fields.Many2one('res.users', string="Người cần phê duyệt", tracking=True)
    

    def action_approve_sale(self):
        if self.state != 'draft':
            raise exceptions.UserError("Chỉ được phê duyệt khi ở trạng thái Nháp!")
        self.write({
            'state': 'waiting_manager',
            'current_approver_id': self.env.ref('sales_team.group_sale_manager').users[:1].id  # Gán user quản lý
        })

    def action_approve_manager(self):
        if self.state != 'waiting_manager':
            raise exceptions.UserError("Chỉ được phê duyệt khi ở trạng thái Chờ Quản lý!")
        self.write({
            'state': 'waiting_director',
            'current_approver_id': self.env.ref('base.group_user').users[:1].id  # Gán user giám đốc
        })

    def action_approve_director(self):
        if self.state != 'waiting_director':
            raise exceptions.UserError("Chỉ được phê duyệt khi ở trạng thái Chờ Giám đốc!")
        self.write({
            'state': 'approved',
            'current_approver_id': False  # Không cần ai phê duyệt nữa
        })

    @api.model
    def create(self, vals_list):
        if not self.env.user.has_group('sales_team.group_sale_salesman'):
            raise exceptions.AccessError("Chỉ Sale được phép tạo hợp đồng.")
        return super(Contract, self).create(vals_list)

    def write(self, vals):
        for contract in self:
            if contract.state in ['approved']:
                raise exceptions.UserError("Không thể chỉnh sửa hợp đồng đã được phê duyệt.")
            
            if contract.state == 'manager_approve' and not self.env.user.has_group('sales_team.group_sale_manager'):
                raise exceptions.AccessError("Chỉ Quản lý bán hàng mới được phép chỉnh sửa hợp đồng ở trạng thái Quản lý phê duyệt.")
            
            if contract.state == 'director_approve' and not self.env.user.has_group('sales_team.group_sale_manager') and not self.env.user.has_group('contract.contract_rule_director'):
                raise exceptions.AccessError("Chỉ Quản lý bán hàng hoặc Giám đốc mới được phép chỉnh sửa hợp đồng ở trạng thái Giám đốc phê duyệt.")
            
            if contract.state == 'draft' and not self.env.user.has_group('sales_team.group_sale_salesman'):
                raise exceptions.AccessError("Chỉ Sale được phép chỉnh sửa hợp đồng ở trạng thái Nháp.")

        return super(Contract, self).write(vals)