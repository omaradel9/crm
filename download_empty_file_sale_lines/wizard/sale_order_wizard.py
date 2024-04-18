from odoo import models, fields, api


class SaleOrderLinesImportWizard(models.TransientModel):
    _inherit = 'sale.order.lines.import.wizard'



 

    


    def action_download_sale_order_line_excel_doc(self):
         return {
            'type': 'ir.actions.act_url',
            'url': '/web/binary/download_document?model=sale.order.lines.import.wizard&id=%s' % (self.id),
            'target': 'new',
        }
      