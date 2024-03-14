from odoo import models, fields, api


class ActivityReportCreateWizard(models.TransientModel):
    _name = 'activity.report.create.wizard'
    _description = 'Activity Report create Wizard'


    name = fields.Char(related='lead_id.name')
    date = fields.Datetime('Completion Date')
    lead_create_date = fields.Datetime('Creation Date')
    date_conversion = fields.Datetime('Conversion Date')
    date_deadline = fields.Date('Expected Closing')
    date_closed = fields.Datetime('Closed Date')
    author_id = fields.Many2one('res.partner', 'Assigned To')
    user_id = fields.Many2one('res.users', 'Salesperson')
    team_id = fields.Many2one('crm.team', 'Sales Team')
    lead_id = fields.Many2one('crm.lead', "Opportunity")
    body = fields.Html('Activity Description')
    subtype_id = fields.Many2one('mail.message.subtype', 'Subtype')
    mail_activity_type_id = fields.Many2one('mail.activity.type', 'Activity Type')
    country_id = fields.Many2one('res.country', 'Country')
    company_id = fields.Many2one('res.company', 'Company')
    stage_id = fields.Many2one('crm.stage', 'Stage')
    partner_id = fields.Many2one('res.partner', 'Customer')
    lead_type = fields.Selection(
        string='Type',
        selection=[('lead', 'Lead'), ('opportunity', 'Opportunity')],
        help="Type is used to separate Leads and Opportunities")
    active = fields.Boolean('Active')




    @api.model
    def default_get(self, fields):
        res = super(ActivityReportCreateWizard, self).default_get(fields)
        lead_id = self.env['ir.config_parameter'].sudo().get_param('crm_custom.crm_lead_id')
        
        if lead_id:
            res['lead_id'] = int(lead_id)
            
        return res    



   





    def action_create_mail_activity(self):
     

        activity_id =  self.env['mail.activity'].create({
                'date_deadline': self.date_deadline,
                'user_id': self.user_id.id,
                'activity_type_id': self.mail_activity_type_id.id,
                'res_model_id': self.env['ir.model'].search([('model', '=', 'crm.lead')]).id,
                'res_id': self.lead_id.id,


        })
        return {
            'type': 'ir.actions.act_window',
            'name': 'Mail Activity',
            'res_model': 'mail.activity',
            'view_mode': 'form',
            'target': 'current',
            'res_id': activity_id.id
        }

    


   
        
