from odoo import fields, models, tools


class ActivityReport(models.Model):
    """ CRM Lead Analysis """

    _inherit = "crm.activity.report"

    crm_attachment_id = fields.One2many('crm.attachments', 'mail_message_id')

    def _select(self):
        return """
            SELECT
                m.id,
                l.create_date AS lead_create_date,
                l.date_conversion,
                l.date_deadline,
                l.date_closed,
                m.subtype_id,
                m.mail_activity_type_id,
                m.author_id,
                m.date,
                m.body,
                l.id as lead_id,
                l.user_id,
                l.team_id,
                l.country_id,
                l.company_id,
                l.stage_id,
                l.partner_id,
                l.type as lead_type,
                l.active,
                a.id as crm_attachment_id
        """

    def _join(self):
        return """
            JOIN crm_lead AS l ON m.res_id = l.id
            LEFT JOIN crm_attachments AS a ON m.id = a.mail_message_id
        """




   



 


    def action_edit_activity(self):
        
    
        return {
            'type': 'ir.actions.act_window',
            'name': 'Activity Report',
            'res_model': 'activity.report.wizard',
            'view_mode': 'form',
            'target': 'new',
        }




    
  





