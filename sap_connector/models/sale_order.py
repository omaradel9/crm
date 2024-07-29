from odoo import fields,models,api
from bs4 import BeautifulSoup




class SaleOrder(models.Model):
    _inherit="sale.order"
    
    ready_to_integrate = fields.Boolean('Ready To Integrate')

    def action_send_to_sap(self):
        for order in self:
            soup = BeautifulSoup(order.payment_term_id.note, 'html.parser')
            note = soup.get_text()

            if not order.partner_id.sap_id:
                    return {
                    'type': 'ir.actions.act_window',
                    'name': 'Add SAP ID',
                    'res_model': 'sap.id.wizard',
                    'view_mode': 'form',
                    'target': 'new',
                    'context': {
                        'default_partner_id': order.partner_id.id,
                        'default_order_id': order.id,
                    },
                }
          
                        
            pro = []     
            for line in order.order_line:
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
                                'default_order_id': order.id,
}

                    }
            
            if not note:
                  return {
                    'type': 'ir.actions.act_window',
                    'name': 'ADD Payment Note',
                    'res_model': 'set.payment.note',
                    'view_mode': 'form',
                    'target': 'new',
                    'context': {
                        'default_order_id': order.id,
                    },

                    }    
                        
                
                
