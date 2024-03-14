from odoo import fields,models,api



class SaleOrderLine(models.Model):
    _inherit="sale.order.line"


    smart_account_mandatory = fields.Char()
    cisco_product_ref = fields.Text(string="Vendor Product Reference")
    product_family = fields.Text(string="Product Family / Service Level")
    estimated_lead_time = fields.Text(string="Estimated Lead Time (Days)")
    cost = fields.Float('Unit Vendor List Price')


    pricing_term  =fields.Text()


    



    @api.depends('product_id', 'product_uom', 'product_uom_qty','cost','discount_metra')
    def _compute_price_unit(self):
        for line in self:
            # check if there is already invoiced amount. if so, the price shouldn't change as it might have been
            # manually edited
            if line.cost :
                line.price_unit = round(line.cost - ((line.cost * line.discount_metra) / 100), 2)

                  
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