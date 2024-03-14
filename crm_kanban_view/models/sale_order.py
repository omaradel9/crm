from odoo import fields,models,api



class SaleOrder(models.Model):
    _inherit="sale.order"



    vendor_id = fields.Many2one('res.partner', string='Vendor', ondelete='restrict',)
    contact_person = fields.Many2one('res.partner',string="Contact Person")

    



 
