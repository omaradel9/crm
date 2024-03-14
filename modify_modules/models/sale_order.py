from odoo import fields,models,api



class SaleOrder(models.Model):
    _inherit="sale.order"



  

    margin = fields.Float(string='Margin')
    vendor_account_manager = fields.Many2one('res.partner',string="Vendor Account Manager" ,
    
    )
    current_company_brands = fields.Selection(string='brands',related='company_id.brands')




    @api.onchange('margin')
    def _compute_order_lines_margin(self):
        for rec in self.order_line:
            rec.mergin = self.margin