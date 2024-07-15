from odoo import fields,models,api



class SaleOrder(models.Model):
    _inherit="sale.order"
    
    
    
    # end_user_industry_id = fields.Many2one('res.partner',related='end_user_id.industry_id',string='End User Industry')
    
    end_user_industry_id = fields.Many2one(string='End User Industry', related='end_user_id.industry_id',readonly=False)
