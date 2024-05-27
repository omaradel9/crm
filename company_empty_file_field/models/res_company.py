from odoo import api,  fields, models, _, Command



class ResCompany(models.Model):
    _inherit = "res.company"





    so_empty_file = fields.Binary(string = 'SO Empty File')