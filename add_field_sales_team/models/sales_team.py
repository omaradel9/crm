from odoo import fields,models,api



class CrmTeam(models.Model):
    _inherit="crm.team"



    
    report_to_ids = fields.Many2many(
        string='Report To',
        comodel_name='res.users',
        relation='crm_team_user_rel',
        column1='crm_id',
        column2='user_id',
    )
    
