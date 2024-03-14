from odoo import fields,models,api



class CrmStage(models.Model):
    _inherit="crm.stage"
    
    
    
    probability = fields.Float()