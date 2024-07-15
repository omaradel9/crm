from odoo import fields,models,api



class CrmLead(models.Model):
    _inherit="crm.lead"
    
    end_user_industry_id = fields.Many2one(string='End User Industry', related='end_user_id.industry_id',store=True)
