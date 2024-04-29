from odoo import fields,models,api



class SaleOrder(models.Model):
    _inherit="sale.order"

    






    @api.onchange('margin')
    def _compute_order_lines_margin(self):
        for rec in self.order_line:
            rec.mergin = self.margin
            rec.price_unit = (rec.unit_net_price * (1+ rec.conditions/100))/(1- rec.mergin/100)



    @api.onchange('term_conditions_id')
    def _get_tax_ids(self):
        for rec in self.order_line:
            rec.tax_id = self.term_conditions_id.tax_id
             