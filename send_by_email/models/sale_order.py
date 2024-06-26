from odoo import fields, models, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    po_no = fields.Char('PO.no')
    def action_quotation_sends(self):

        MCM = self.env['mail.compose.message']
        so_mcm_vals = self.action_quotation_send().get('context', {})
        # Create record of compose mail
        compose_msg = MCM.with_context(so_mcm_vals).create({})
        compose_msg._onchange_template_id_wrapper()
        compose_msg.action_send_mail()
    def _find_mail_template(self):
        """ Get the appropriate mail template for the current sales order based on its state.

        If the SO is confirmed, we return the mail template for the sale confirmation.
        Otherwise, we return the quotation email template.

        :return: The correct mail template based on the current status
        :rtype: record of `mail.template` or `None` if not found
        """
        self.ensure_one()
        if self.env.context.get('proforma') or self.state not in ('sale', 'done'):
            return self.env.ref('send_by_email.email_template_custom_quotation_sale', raise_if_not_found=False)
        else:
            return self._get_confirmation_template()
        


    def _get_confirmation_template(self):
        """ Get the mail template sent on SO confirmation (or for confirmed SO's).

        :return: `mail.template` record or None if default template wasn't found
        """
        return self.env.ref('send_by_email.mail_template_custom_sale_confirmation', raise_if_not_found=False)    