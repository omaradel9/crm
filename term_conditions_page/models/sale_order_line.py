from odoo import fields,models,api



class SaleOrder(models.Model):
    _inherit="sale.order.line"



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
    

    name = fields.Text(
        string="Product Description",
        compute='_compute_name',
        store=True, readonly=False, required=True, precompute=True)
    

    duration = fields.Char(
        string='Service Duration (Months)',
    )

    price_unit = fields.Float(
        string="Unit Net Price",
        compute='_compute_price_unit',
        digits='Product Price',
        store=True, readonly=False, required=True, precompute=True)
    

    price_subtotal = fields.Monetary(
        string="Total Price",
        compute='_compute_amount',
        store=True, precompute=True)
    

    discount_metra = fields.Float('Vendor Discount (%)')



