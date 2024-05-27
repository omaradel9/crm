from odoo import models, fields, api
from odoo.exceptions import ValidationError


class SaleOrderLinesImportWizard(models.TransientModel):
    _inherit = 'sale.order.lines.import.wizard'








 

    


    def action_download_sale_order_line_excel_doc(self):
        if self.order_id.company_empty_file:
                return {
                    'type': 'ir.actions.act_url',
                    'url': '/web/binary/download_document?model=sale.order.lines.import.wizard&id=%s&order_id=%s' % (self.id, self.order_id.id),
                    'target': 'new',
                }
         
        else:
            raise ValidationError("Your Company Dose Not Have Template")
 