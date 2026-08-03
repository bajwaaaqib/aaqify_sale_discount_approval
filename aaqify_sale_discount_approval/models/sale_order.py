from odoo import models, fields, _

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def write(self, vals):
        """Monitor line discount changes. If discount is reduced below threshold, clean up pending activities."""
        res = super().write(vals)

        # Check if order lines or discounts were modified
        if 'order_line' in vals:
            for order in self:
                if order.state in ['draft', 'sent']:
                    max_discount = max(order.order_line.mapped('discount') or [0.0])

                    # Find if any rule is still violated
                    rules = self.env['sale.discount.approval'].search([
                        ('company_ids', 'in', [order.company_id.id]),
                        ('percentage', '<', max_discount)
                    ])

                    # If discount was reduced so NO rule is violated anymore, remove pending activities
                    if not rules:
                        order._cancel_discount_approval_activities()

        return res

    def action_confirm(self):
        """Handle confirmation logic and auto-complete or clear activities."""
        for order in self:
            max_discount = max(order.order_line.mapped('discount') or [0.0])

            if max_discount > 0.0:
                rules = self.env['sale.discount.approval'].search([
                    ('company_ids', 'in', [order.company_id.id]),
                    ('percentage', '<', max_discount)
                ])

                if rules:
                    authorized_user_ids = set(rules.mapped('user_ids').ids)

                    # 1. NON-AUTHORIZED USER tries to confirm -> BLOCK & CREATE ACTIVITY
                    if self.env.user.id not in authorized_user_ids:
                        order._schedule_approval_activities_isolated(rules, max_discount)

                        return {
                            'type': 'ir.actions.client',
                            'tag': 'display_notification',
                            'params': {
                                'title': _("Approval Required"),
                                'message': _(
                                    "Discount (%.2f%%) exceeds configured limit. "
                                    "An approval activity has been assigned to authorized managers."
                                ) % max_discount,
                                'type': 'warning',
                                'sticky': True,
                                'next': {
                                    'type': 'ir.actions.client',
                                    'tag': 'reload',
                                }
                            }
                        }

                    # 2. AUTHORIZED USER confirms order -> MARK ACTIVITY AS DONE
                    else:
                        order._complete_discount_approval_activities()

        # Proceed with standard confirmation
        res = super().action_confirm()

        # Cleanup any remaining pending discount activities after confirmation
        for order in self:
            order._cancel_discount_approval_activities()

        return res

    def _schedule_approval_activities_isolated(self, rules, max_discount):
        """Creates activities using an isolated cursor so it persists immediately."""
        with self.pool.cursor() as new_cr:
            new_env = self.env(cr=new_cr)
            activity_type = new_env.ref('mail.mail_activity_data_todo', raise_if_not_found=False)
            sale_model_id = new_env.ref('sale.model_sale_order').id

            if not activity_type:
                return

            for rule in rules:
                for user_id in rule.user_ids.ids:
                    existing_activity = new_env['mail.activity'].search([
                        ('res_model', '=', 'sale.order'),
                        ('res_id', '=', self.id),
                        ('user_id', '=', user_id),
                        ('summary', '=', _('High Discount Approval Required'))
                    ], limit=1)

                    if not existing_activity:
                        new_env['mail.activity'].create({
                            'activity_type_id': activity_type.id,
                            'summary': _('High Discount Approval Required'),
                            'note': _(
                                "Order <b>%s</b> discount (<b>%.2f%%</b>) exceeds limit (<b>%.2f%%</b>)."
                            ) % (self.name, max_discount, rule.percentage),
                            'user_id': user_id,
                            'res_id': self.id,
                            'res_model_id': sale_model_id,
                        })
            new_cr.commit()

    def _complete_discount_approval_activities(self):
        """Marks pending discount approval activities as Done."""
        activities = self.env['mail.activity'].search([
            ('res_model', '=', 'sale.order'),
            ('res_id', 'in', self.ids),
            ('summary', '=', _('High Discount Approval Required'))
        ])
        if activities:
            activities.action_feedback(feedback=_("Approved and confirmed by manager."))

    def _cancel_discount_approval_activities(self):
        """Deletes/Cancels pending discount approval activities."""
        activities = self.env['mail.activity'].search([
            ('res_model', '=', 'sale.order'),
            ('res_id', 'in', self.ids),
            ('summary', '=', _('High Discount Approval Required'))
        ])
        if activities:
            activities.unlink()