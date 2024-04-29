from odoo import models, api, fields



class TermsConditionsSales(models.Model):
    _inherit = "terms.condtions.sales"



    payment_method = fields.Text('Payment Method')
    incoterms = fields.Html('Incoterms')
