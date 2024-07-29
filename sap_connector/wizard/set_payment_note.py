from odoo import models, fields, api

class SetPaymentNote(models.TransientModel):
    _name = 'set.payment.note'
    
    order_id = fields.Many2one('sale.order', string="order", required=True)
    payment_note = fields.Char()
    
    
    
    def action_confirm(self):
        self.ensure_one()
        if self.order_id:
            self.order_id.payment_term_id.note = self.payment_note
        