from odoo import fields,models,api



class SaleOrderLine(models.Model):
    _inherit="sale.order.line"


    smart_account_mandatory = fields.Char()
    cisco_product_ref = fields.Text(string="Vendor Product Reference")
    product_family = fields.Text(string="Product Family / Service Level")
    estimated_lead_time = fields.Text(string="Estimated Lead Time (Days)")
    cost = fields.Float('Unit Vendor List Price')


    pricing_term  =fields.Text()


    



   