from odoo import fields,models,api

class SaleOrder(models.Model):
    _inherit="sale.order"

    sap_quotation_no = fields.Char()
    message = fields.Text()
    sap_status = fields.Selection(
        string='Sap Status',
        default='not_sent',
        selection=[('request_sent', 'Request Sent'), ('not_sent', 'Not Sent')],
        compute='_compute_ready_to_integrate',store=True
    )
    ready_to_integrate = fields.Boolean('Ready To Integrate',compute='onchange_sap_status',store=True)

    @api.depends('ready_to_integrate')
    def _compute_ready_to_integrate(self):
        for rec in self:
            if rec.ready_to_integrate:
                rec.sap_status = 'request_sent'
            else:
                rec.sap_status = 'not_sent'
                
                
    @api.depends('state')
    def onchange_sap_status(self):
        for rec in self:
            if rec.state == 'draft' or rec.state == 'cancel' :
                rec.ready_to_integrate = False
            else:
                rec.ready_to_integrate = True

                    
           
             
    