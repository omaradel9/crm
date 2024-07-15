from odoo import fields,models,api
from collections import defaultdict
from datetime import timedelta

from odoo.exceptions import UserError
from odoo.fields import Command
from odoo.osv import expression
from odoo.tools import float_is_zero, float_compare, float_round


class SaleOrder(models.Model):
    _inherit="sale.order.line"


    alt_barcode = fields.Char('Metra Code', related='product_template_id.default_code')
    product_template_id = fields.Many2one(
        string="MPN",
        comodel_name='product.template',
        compute='_compute_product_template_id',
        readonly=False,
        search='_search_product_template_id',
        # previously related='product_id.product_tmpl_id'
        # not anymore since the field must be considered editable for product configurator logic
        # without modifying the related product_id when updated.
        domain=[('sale_ok', '=', True)])
  
    



    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('display_type') or self.default_get(['display_type']).get('display_type'):
                vals['product_uom_qty'] = 0.0
           

        lines = super().create(vals_list)
        for line in lines:
            if line.product_uom_qty != 0:
                line.unit_net_price = round(line.total_price / line.product_uom_qty, 2)
            else:
                line.unit_net_price = 0
            # line.unit_net_price  = round(line.total_price/line.product_uom_qty,2)

            line.partner_unit_net_price  = round(line.unit_net_price-(line.unit_net_price*(line.partner_discount/100)),2)
            line.price_unit = (line.unit_net_price * (1+ line.conditions/100))/(1- line.mergin/100) 

            if line.product_id and line.state == 'sale':
                msg = _("Extra line with %s", line.product_id.display_name)
                line.order_id.message_post(body=msg)
                # create an analytic account if at least an expense product
                if line.product_id.expense_policy not in [False, 'no'] and not line.order_id.analytic_account_id:
                    line.order_id._create_analytic_account()
                  
        return lines
    


  
    



    @api.onchange('mergin','conditions','total_price','partner_discount','product_uom_qty','discount_metra')
    def _compute_order_lines_values(self):


       
        self.unit_net_price  = round(self.total_price/self.product_uom_qty,2)

        self.partner_unit_net_price  = round(self.unit_net_price-(self.unit_net_price*(self.partner_discount/100)),2)
        self.price_unit = (self.unit_net_price * (1+ self.conditions/100))/(1- self.mergin/100) 
       
    





   