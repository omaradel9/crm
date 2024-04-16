from odoo import fields,models,api



class SaleOrderLine(models.Model):
    _inherit="sale.order.line"


    conditions = fields.Float(string='Conditions (%)')

    



    @api.depends('product_id', 'product_uom', 'product_uom_qty','unit_net_price','mergin')
    def _compute_price_unit(self):
        for line in self:
            # check if there is already invoiced amount. if so, the price shouldn't change as it might have been
            # manually edited
            if line.unit_net_price :
                line.price_unit = (line.unit_net_price * (1+ line.conditions/100))/(1- line.mergin/100) 


                  
            elif line.qty_invoiced > 0:
                continue
            elif not line.product_uom or not line.product_id or not line.order_id.pricelist_id:
                line.price_unit = 0.0
            else:
                price = line.with_company(line.company_id)._get_display_price()
                line.price_unit = line.product_id._get_tax_included_unit_price(
                    line.company_id,
                    line.order_id.currency_id,
                    line.order_id.date_order,
                    'sale',
                    fiscal_position=line.order_id.fiscal_position_id,
                    product_price_unit=price,
                    product_currency=line.currency_id
                )
