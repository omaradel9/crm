from odoo import fields,models,api



class SaleOrder(models.Model):
    _inherit="product.template"


    name = fields.Char('MPN', index='trigram', required=True, translate=True)

    default_code = fields.Char(
        'Material Number', compute='_compute_default_code',
        inverse='_set_default_code', store=True)



