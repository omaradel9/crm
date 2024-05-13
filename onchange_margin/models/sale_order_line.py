from odoo import fields,models,api
from collections import defaultdict
from datetime import timedelta

from odoo.exceptions import UserError
from odoo.fields import Command
from odoo.osv import expression
from odoo.tools import float_is_zero, float_compare, float_round


class SaleOrder(models.Model):
    _inherit="sale.order.line"


    alt_barcode = fields.Char('Metra Code', related='product_template_id.alt_barcode')
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
            print('--------------------------------------wrrrrrrrrrrrrrrrrrrrrrrrr22222222222222222222',line.cost) 
            line.unit_net_price  = round(line.cost - ((line.cost * line.discount_metra) / 100), 2)

            line.total_price = round((line.unit_net_price * line.product_uom_qty), 2)
            line.partner_unit_net_price  = round(line.cost - (line.cost * (line.partner_discount / 100)), 2)
            line.price_unit = (line.unit_net_price * (1+ line.conditions/100))/(1- line.mergin/100)     

            if line.product_id and line.state == 'sale':
                msg = _("Extra line with %s", line.product_id.display_name)
                line.order_id.message_post(body=msg)
                # create an analytic account if at least an expense product
                if line.product_id.expense_policy not in [False, 'no'] and not line.order_id.analytic_account_id:
                    line.order_id._create_analytic_account()
                  
        return lines
    


    def write(self, values):
        if 'display_type' in values and self.filtered(lambda line: line.display_type != values.get('display_type')):
            raise UserError(_("You cannot change the type of a sale order line. Instead you should delete the current line and create a new line of the proper type."))

        if 'product_uom_qty' in values:
            precision = self.env['decimal.precision'].precision_get('Product Unit of Measure')
            self.filtered(
                lambda r: r.state == 'sale' and float_compare(r.product_uom_qty, values['product_uom_qty'], precision_digits=precision) != 0)._update_line_quantity(values)

        # Prevent writing on a locked SO.
        protected_fields = self._get_protected_fields()
        if 'done' in self.mapped('state') and any(f in values.keys() for f in protected_fields):
            protected_fields_modified = list(set(protected_fields) & set(values.keys()))

            if 'name' in protected_fields_modified and all(self.mapped('is_downpayment')):
                protected_fields_modified.remove('name')

            fields = self.env['ir.model.fields'].sudo().search([
                ('name', 'in', protected_fields_modified), ('model', '=', self._name)
            ])
            if fields:
                raise UserError(
                    _('It is forbidden to modify the following fields in a locked order:\n%s')
                    % '\n'.join(fields.mapped('field_description'))
                )
         

        result = super().write(values)

        # Don't recompute the package_id if we are setting the quantity of the items and the quantity of packages
        if 'product_uom_qty' in values and 'product_packaging_qty' in values and 'product_packaging_id' not in values:
            self.env.remove_to_compute(self._fields['product_packaging_id'], self)

        return result
    



    @api.onchange('mergin','conditions','cost','partner_discount','product_uom_qty','discount_metra')
    def _compute_order_lines_values(self):
        print('----------------------change', self.cost)


        self.unit_net_price  = round(self.cost - ((self.cost * self.discount_metra) / 100), 2)

        self.total_price = round((self.unit_net_price * self.product_uom_qty), 2)
        self.partner_unit_net_price  = round(self.cost - (self.cost * (self.partner_discount / 100)), 2)
        self.price_unit = (self.unit_net_price * (1+ self.conditions/100))/(1- self.mergin/100)
       
    





   