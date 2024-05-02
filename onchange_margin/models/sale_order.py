from odoo import fields,models,api



class SaleOrder(models.Model):
    _inherit="sale.order"




    def write(self, values): 
            for rec in self.order_line:
                print('--------------------1111111111111', rec.id)
 
                rec.unit_net_price  = round(rec.cost - ((rec.cost * rec.discount_metra) / 100), 2)

                rec.total_price = round((rec.unit_net_price * rec.product_uom_qty), 2)
                rec.partner_unit_net_price  = round(rec.cost - (rec.cost * (rec.partner_discount / 100)), 2)
                rec.price_unit = (rec.unit_net_price * (1+ rec.conditions/100))/(1- rec.mergin/100)
            result = super().write(values)
            return result
      



           



    
   






    






    @api.onchange('margin')
    def _compute_order_lines_margin(self):
        for rec in self.order_line:
            rec.mergin = self.margin
            rec.price_unit = (rec.unit_net_price * (1+ rec.conditions/100))/(1- rec.mergin/100) # new push



    @api.onchange('term_conditions_id')
    def _get_tax_ids(self):
        for rec in self.order_line:
            rec.tax_id = self.term_conditions_id.tax_id
             