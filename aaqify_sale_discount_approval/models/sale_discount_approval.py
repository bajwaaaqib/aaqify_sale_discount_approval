from odoo import models, fields

class SaleDiscountApproval(models.Model):
    _name = 'sale.discount.approval'
    _description = 'Sale Discount Approval Rule'

    name = fields.Char(string='Rule Name', required=True)
    percentage = fields.Float(string='Discount Percentage Threshold (%)', required=True)

    user_ids = fields.Many2many(
        comodel_name='res.users',
        relation='sale_discount_approval_user_rel',
        column1='approval_id',
        column2='user_id',
        string='Authorised Approvers',
        required=True
    )

    company_ids = fields.Many2many(
        comodel_name='res.company',
        relation='sale_discount_approval_company_rel',
        column1='approval_id',
        column2='company_id',
        string='Applicable Companies',
        required=True,
        default=lambda self: [self.env.company.id]
    )