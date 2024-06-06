from odoo import fields,models,api



class RseCompany(models.Model):
    _inherit="res.company"


    
    company_code = fields.Integer('Company Code')
    
