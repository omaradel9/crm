
from collections import defaultdict

from odoo import api,  fields, models, _, Command



class MailActivity(models.Model):
    _inherit = "mail.activity"

    lead_id = fields.Many2one('crm.lead', "Opportunity", readonly=True)
    
    attachment_ids = fields.One2many(
        string='Attachment',
        comodel_name='crm.attachments',
        inverse_name='activity_id',
    )
    

    @api.model
    def default_get(self, fields):
        res = super(MailActivity, self).default_get(fields)

        lead_id = self.env['ir.config_parameter'].sudo().get_param('crm_custom.crm_lead_id')

        if lead_id:
            res['lead_id'] = int(lead_id)
            res['res_model_id'] = self.env['ir.model']._get_id('crm.lead')
            res['res_id'] = res['lead_id']   

        return res
    

      
    


    def _action_done(self, feedback=False, attachment_ids=None):
     


            
        # marking as 'done'
        messages = self.env['mail.message']
        next_activities_values = []

        # Search for all attachments linked to the activities we are about to unlink. This way, we
        # can link them to the message posted and prevent their deletion.
        attachments = self.env['ir.attachment'].search_read([
            ('res_model', '=', self._name),
            ('res_id', 'in', self.ids),
        ], ['id', 'res_id'])

        activity_attachments = defaultdict(list)
        for attachment in attachments:
            activity_id = attachment['res_id']
            activity_attachments[activity_id].append(attachment['id'])

        for model, activity_data in self._classify_by_model().items():
            records = self.env[model].browse(activity_data['record_ids'])
            for record, activity in zip(records, activity_data['activities']):
                # extract value to generate next activities
                if activity.chaining_type == 'trigger':
                    vals = activity.with_context(activity_previous_deadline=activity.date_deadline)._prepare_next_activity_values()
                    next_activities_values.append(vals)

                # post message on activity, before deleting it
                activity_message = record.message_post_with_view(
                    'mail.message_activity_done',
                    values={
                        'activity': activity,
                        'feedback': feedback,
                        'display_assignee': activity.user_id != self.env.user
                    },
                    subtype_id=self.env['ir.model.data']._xmlid_to_res_id('mail.mt_activities'),
                    mail_activity_type_id=activity.activity_type_id.id,
                    attachment_ids=[Command.link(attachment_id) for attachment_id in attachment_ids] if attachment_ids else [],
                )

                # Moving the attachments in the message
                # TODO: Fix void res_id on attachment when you create an activity with an image
                # directly, see route /web_editor/attachment/add
                if activity_attachments[activity.id]:
                    message_attachments = self.env['ir.attachment'].browse(activity_attachments[activity.id])
                    if message_attachments:
                        message_attachments.write({
                            'res_id': activity_message.id,
                            'res_model': activity_message._name,
                        })
                        activity_message.attachment_ids = message_attachments
                messages += activity_message
                if messages:  
                    if not attachment_ids:
                        attachments = self.attachment_ids.ids
                        messages.write({'crm_attachment_id': [(6, 0, attachments)]})

        next_activities = self.env['mail.activity']
        if next_activities_values:
            next_activities = self.env['mail.activity'].create(next_activities_values)
           

        self.unlink()  # will unlink activity, dont access `self` after that

       
        

      

       
                
        return messages, next_activities        

    


 