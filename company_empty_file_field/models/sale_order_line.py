from odoo import api,  fields, models, _, Command



class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"




    last_date_of_support = fields.Char(
        string='Last Date of Support',
    )

    serial_number = fields.Char(
        string='PAK/Serial Number',
    )
    start_date = fields.Char(
        string='Start Date',
    )
    end_date = fields.Char(
        string='End Date',
    )

    product_number = fields.Char()
    