from odoo import fields,models,api



class SaleOrderLine(models.Model):
    _inherit="sale.order.line"


    partner_unit_net_price = fields.Float(string='Partner Unit Net Price', compute = '_compute_partner_unit_net_price')
    partner_discount= fields.Float(string='Partner Discount (%)')
    unit_net_price = fields.Float(string='Unit Net Price', compute='_compute_unit_net_price')
    total_price = fields.Float(string='Total Price', compute='_compute_total_price')




    @api.depends('cost','partner_discount')
    def _compute_partner_unit_net_price(self):
        for line in self:
            self.partner_unit_net_price = round(line.cost - (line.cost * (line.partner_discount / 100)), 2)




    @api.depends('product_id', 'product_uom', 'product_uom_qty','unit_net_price','mergin')
    def _compute_price_unit(self):
        for line in self:
            # check if there is already invoiced amount. if so, the price shouldn't change as it might have been
            # manually edited
            if line.unit_net_price :
                line.price_unit = line.unit_net_price * (1+ line.mergin / 100) 

                  
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
    
                        







    @api.depends('cost','discount_metra')
    def _compute_unit_net_price(self):
        for line in self:
            self.unit_net_price = round(line.cost - (line.cost * (line.discount_metra / 100)), 2)

    @api.depends('product_uom_qty','unit_net_price')
    def _compute_total_price(self):
        for line in self:
            self.total_price = round((line.product_uom_qty * line.unit_net_price),2)     
