from odoo import fields,models,api



class ProductTemplate(models.Model):
    _inherit="product.template"




    b_u= fields.Many2one('res.company', 'B.U',default=lambda self: self.env.company)