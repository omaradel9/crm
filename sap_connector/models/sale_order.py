from odoo import fields,models,api



class SaleOrder(models.Model):
    _inherit="sale.order"
    
    ready_to_integrate = fields.Boolean('Ready To Integrate')
    
    def action_send_to_sap(self):
        for order in self:
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
                
                
