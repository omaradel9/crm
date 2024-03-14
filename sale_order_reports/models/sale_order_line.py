from odoo import models, api, fields



class saleOrderLine(models.Model):
    _inherit = "sale.order.line"




    
    
    duration = fields.Char(
        string='Duration',
    )

    line_number = fields.Char()
    discount_metra = fields.Float('Disc (%)')
    special_discount = fields.Float()
    mergin = fields.Float("margin")

    
    