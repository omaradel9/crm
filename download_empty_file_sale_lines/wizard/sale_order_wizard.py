from odoo import models, fields, api


class SaleOrderLinesImportWizard(models.TransientModel):
    _inherit = 'sale.order.lines.import.wizard'








 

    


    def action_download_sale_order_line_excel_doc(self):
         return {
            'type': 'ir.actions.act_url',
            'url': '/web/binary/download_document?model=sale.order.lines.import.wizard&id=%s&order_id=%s' % (self.id, self.order_id.id),
            'target': 'new',
        }
    

    def download_order_lines(self):
        return {
            'type': 'ir.actions.act_url',
            'url': '/web/binary/download_document_with_data?model=sale.order.lines.import.wizard&id=%s&order_id=%s' % (self.id, self.order_id.id),
            'target': 'new',
        }
      
      