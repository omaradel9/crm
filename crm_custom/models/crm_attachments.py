from odoo import models, api, fields



class CrmAttachment(models.Model):
    _name = "crm.attachments"
    
    
    
    name = fields.Char(string="Attachment Name")
    attachment = fields.Binary(string="Attachment")
    mail_message_id = fields.Many2one('mail.message')
    activity_id = fields.Many2one('mail.activity')
    
   
    
    


   