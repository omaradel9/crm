from odoo import fields,models,api



class SaleOrder(models.Model):
    _inherit="sale.order"

    vendor_id = fields.Many2one('res.partner', string='Vendor',domain="[('parent_id','=', False)]", ondelete='restrict',)

  
    
    offer_validity = fields.Text(
        string='Offer Validity',
    )
    prices = fields.Text(
        string='prices',
    )

 
    
    delivery = fields.Text(
        string='Delivery',
    )
    partial_delivery = fields.Text(
        string='Partial Delivery',
    )
    responsibility = fields.Text(
        string='Responsibility',
    )
    required_information = fields.Text(
        string='Required Information',
    )


  




    @api.onchange('vendor_id')
    def _get_vendor_account_manager(self):
        if self.vendor_account_manager.parent_id.id != self.vendor_id.id:
               self.vendor_account_manager=False

    @api.onchange('partner_id')
    def _get_contact_person(self):
        if self.contact_person.parent_id.id != self.partner_id.id:
               self.contact_person=False           






    @api.onchange('term_conditions_id')
    def _get_payment_terms(self):
        self.payment_term_id = self.term_conditions_id.payment_id.id
        self.offer_validity = self.term_conditions_id.offer_validity
        self.prices = self.term_conditions_id.prices
        self.delivery = self.term_conditions_id.delivery
        self.partial_delivery = self.term_conditions_id.partial_delivery
        self.responsibility = self.term_conditions_id.responsibility
        self.required_information = self.term_conditions_id.required_information
