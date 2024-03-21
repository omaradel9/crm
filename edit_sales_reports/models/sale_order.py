from odoo import fields,models,api
# from odoo.tools import amount_to_text
from num2words import num2words




class SaleOrder(models.Model):
    _inherit="sale.order"

    delivery_location = fields.Text('Delivery Location')
    mode_of_shipment = fields.Text('Mode of Shipment')

    payment_method = fields.Text('Payment Method')
    incoterms = fields.Text('Incoterms')
    user_id = fields.Many2one(
        comodel_name='res.users',
        string="Salesperson",
        compute='_compute_user_id',
        store=True, readonly=False,required=True, precompute=True, index=True,
        tracking=2,
        domain=lambda self: "[('groups_id', '=', {}), ('share', '=', False), ('company_ids', '=', company_id)]".format(
            self.env.ref("sales_team.group_sale_salesman").id
        ))



    @api.onchange('term_conditions_id')
    def _get_terms_conditions(self):
        self.payment_term_id = self.term_conditions_id.payment_id.id
        self.offer_validity = self.term_conditions_id.offer_validity
        self.prices = self.term_conditions_id.prices
        self.delivery = self.term_conditions_id.delivery
        self.partial_delivery = self.term_conditions_id.partial_delivery
        self.responsibility = self.term_conditions_id.responsibility
        self.required_information = self.term_conditions_id.required_information
        self.payment_method = self.term_conditions_id.payment_method
        self.incoterms = self.term_conditions_id.incoterms





    @api.depends('amount_total')
    def compute_total_text(self):
        total_text = num2words(self.amount_total).upper()

        return  total_text   
     