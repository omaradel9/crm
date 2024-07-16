from odoo import models, fields, api

class SAPIDWizard(models.TransientModel):
    _name = 'sap.id.wizard'

    partner_id = fields.Many2one('res.partner', string="Partner", required=True)
    order_id = fields.Many2one('sale.order', string="order", required=True)
    sap_id = fields.Char(string="SAP ID", required=True)

    def action_confirm(self):
        self.ensure_one()
        if self.partner_id.parent_id:
            self.partner_id.parent_id.sap_id = self.sap_id
            self.order_id.ready_to_integrate = True
        else:
            self.partner_id.sap_id = self.sap_id
            self.order_id.ready_to_integrate = True
        return {'type': 'ir.actions.act_window_close'}