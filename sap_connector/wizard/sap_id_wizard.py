from odoo import models, fields, api
from bs4 import BeautifulSoup


class SAPIDWizard(models.TransientModel):
    _name = 'sap.id.wizard'

    partner_id = fields.Many2one('res.partner', string="Partner", required=True)
    order_id = fields.Many2one('sale.order', string="order", required=True)
    sap_id = fields.Char(string="SAP ID", required=True)

    def action_confirm(self):
        self.ensure_one()
        if self.partner_id.parent_id:
            self.partner_id.parent_id.sap_id = self.sap_id
            self.order_id.ready_to_integrate = True
        else:
            self.partner_id.sap_id = self.sap_id
            self.order_id.ready_to_integrate = True
        pro = []
        for line in self.order_id.order_line:
                if not line.alt_barcode and line.display_type != 'line_section':
                    pro.append(line.product_template_id.id)
        if len(pro):
            return {
                'type': 'ir.actions.act_window',
                'name': 'ADD Material Number',
                'res_model': 'set.default.code.product',
                'view_mode': 'form',
                'target': 'new',
                'context': {'default_sale_order_line_ids': [{'product_template_id': p} for p in pro],
                            'default_order_id': self.order_id.id,
}
                }
        soup = BeautifulSoup(self.order_id.payment_term_id.note, 'html.parser')
        note = soup.get_text()  
        if not note:
      
            return {
                'type': 'ir.actions.act_window',
                'name': 'ADD Payment Note',
                'res_model': 'set.payment.note',
                'view_mode': 'form',
                'target': 'new',
                'context': {
                    'default_order_id': self.order_id.id,
                },

                }       