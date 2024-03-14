from odoo import models, api, fields



class TermsConditionsSales(models.Model):
    _name = "terms.condtions.sales"




    
    name = fields.Char(
        string='name',
    )
    
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


    tax = fields.Char(
        string='Tax'
    )

    
    payment = fields.Html()
    
    
    
    
    
    