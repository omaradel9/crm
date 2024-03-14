from odoo import models, api, fields



class SaleOrder(models.Model):
    _inherit = "sale.order"




    
    
    
    def open_order_line_wizard_custom(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Import Order Lines',
            'res_model': 'sale.order.lines.import.wizard',
            'view_mode': 'form',
            'target': 'new',
        }


  






  

    
    
    
    
    