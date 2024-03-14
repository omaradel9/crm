from odoo import fields,models,api



class ResPartner(models.Model):
    _inherit="res.partner"



    
    end_user = fields.Boolean(string='End User',)
    vendor = fields.Boolean(string='Vendor',)
    customer = fields.Boolean(
        string='Customer',
    )