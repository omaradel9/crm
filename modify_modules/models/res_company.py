from odoo import models, api, fields



class ResCompany(models.Model):
    _inherit = "res.company"



    
    brands = fields.Selection(
        string='brands',
        selection=[('cisco', 'Cisco'), ('hp', 'hp'), ('dell','Dell')]
    )