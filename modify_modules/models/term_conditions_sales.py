from odoo import models, api, fields



class TermsConditionsSales(models.Model):
    _inherit= "terms.condtions.sales"


    tax_id = fields.Many2one('account.tax')
    payment_id = fields.Many2one('account.payment.term', string='Payment')

    tax = fields.Char(
        string='Tax',related='tax_id.name'
    )

    
    payment = fields.Html(related='payment_id.note')

