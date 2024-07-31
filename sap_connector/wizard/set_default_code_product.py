from odoo import models, fields, api
from bs4 import BeautifulSoup


class SetDefaultCodeProduct(models.TransientModel):
    _name = 'set.default.code.product'
    
    order_id = fields.Many2one('sale.order', string="order", required=True)

    sale_order_line_ids = fields.One2many(
        string='Set Material Number',
        comodel_name='sale.order.line.wizard',
        inverse_name='set_default_code_id',
    )
    
    def action_confirm(self):
        self.ensure_one()
        
        for line in self.sale_order_line_ids:
            product = self.env['product.template'].search([('id', '=', line.product_template_id.id)])
            if product:
                product.write({
                    'default_code': line.default_code,
                })
        note_content = self.order_id.payment_term_id.note
        if isinstance(note_content, str):
            soup = BeautifulSoup(note_content, 'html.parser')
            note = soup.get_text()
            # self.order_id.ready_to_integrate = True

        else:
            note = ''

        if not note:
            return {
                'type': 'ir.actions.act_window',
                'name': 'ADD Payment Note',
                'res_model': 'set.payment.note',
                'view_mode': 'form',
                'target': 'new',
                'context': {
                    'default_order_id': self.order_id.id,
                },
            }        
          
  
class SalesOrderLineWizard(models.TransientModel):
    _name = 'sale.order.line.wizard'


    set_default_code_id = fields.Many2one(
        string='set default code',
        comodel_name='set.default.code.product',
        ondelete='restrict',
    )
    product_id = fields.Many2one(
        comodel_name='product.product',
        string="Product",
        change_default=True, ondelete='restrict',)
    product_template_id = fields.Many2one(
        'product.template',string="Product Template",)
    default_code = fields.Char(
        string="Material Number")    
    