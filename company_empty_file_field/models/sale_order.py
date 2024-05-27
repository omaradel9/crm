from odoo import api,  fields, models, _, Command



class SaleOrder(models.Model):
    _inherit = "sale.order"





    company_empty_file = fields.Binary(related='company_id.so_empty_file')