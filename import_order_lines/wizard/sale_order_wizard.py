from odoo import models, fields, api
import base64
import io
import pandas as pd
from odoo.exceptions import  ValidationError
from odoo.exceptions import  UserError
from odoo.exceptions import Warning

import tempfile
import binascii
import xlrd

class SaleOrderLinesImportWizard(models.TransientModel):
    _name = 'sale.order.lines.import.wizard'



    order_lines_file = fields.Binary(
        string='Upload Order Lines',
    )
    order_id = fields.Many2one('sale.order')
    import_lines_types = fields.Selection([('update_lines', 'Update Lines'), ('add_lines', 'Add Lines')],
                                          default="update_lines", string='Import Lines Type')



    @api.model
    def default_get(self, fields):
        res = super(SaleOrderLinesImportWizard, self).default_get(fields)
        active_id = self._context.get('active_id')
        if active_id:
            res['order_id'] = active_id
        return res

    


    def action_download_sale_order_line_excel_doc(self):
        return self.env.ref('import_order_lines.custom_import_line_action_report_xlsx').report_action(self, data={
            'order_id': False
        })
    


    def download_order_lines(self):
        return self.env.ref('import_order_lines.custom_import_line_action_report_xlsx').report_action(self,
            data={
            'order_id': self.order_id.id,})
    






    def action_import_sale_order_line(self):
        if self.order_lines_file:
            sale_order_line_data = base64.b64decode(self.order_lines_file)
            file_like_object = io.BytesIO(sale_order_line_data)
            data = pd.read_excel(file_like_object)
            df = pd.DataFrame(data)

            tax_list = []
            if self.order_id:
                line_id = self.env['sale.order.line'].search([('order_id', '=', self.order_id.id)])
                line_id.unlink()
            for index, row in df.iterrows():
                product_id = self.env['product.product'].search([('name', '=', row[1])])
                if not product_id:
                    product_id = self.env['product.product'].create({'name': row[1]})
                
            
                    

    
                if self.order_id.current_company_brands == 'cisco':
                        if pd.isnull(row[1]):
                                sale_order_line_values = {
                                    'order_id': self.order_id.id,
                                    'display_type': 'line_section',
                                    'name': row[0],
                                   
                                }
                                sale_order_line = self.env['sale.order.line'].create(sale_order_line_values) 
                        else:        
                            if pd.isnull(row[11]):
                                list_price =0 if pd.isnull([row[8]]) else float(row[8])
                                dic_metra = 0 if pd.isnull([row[12]]) else float(row[12])
                                unit_price_cisco  = round(list_price - ((list_price * dic_metra) / 100), 2)
                        
                                sale_order_line_values = {
                                        'order_id': self.order_id.id,
                                        'line_number':' ' if pd.isnull([row[0]]) else row[0],
                                        'product_id': product_id.id,
                                        'smart_account_mandatory':'' if pd.isnull([row[2]]) else row[2] ,
                                        'name': row[3],
                                        'cisco_product_ref':'' if pd.isnull([row[4]]) else row[4],
                                        'product_family': '' if pd.isnull([row[5]]) else row[5],
                                        'duration': 'N/A' if pd.isnull(row[6]) else row[6],
                                        'estimated_lead_time': 'N/A' if pd.isnull(row[7]) else row[7],
                                        'cost': 0 if pd.isnull(row[8]) else float(row[8]),
                                        'pricing_term': '' if pd.isnull([row[9]]) else row[9],
                                        'product_uom_qty': float(row[10]),
                                        'price_unit':unit_price_cisco, 
                                        'discount_metra': 0 if pd.isnull(row[12]) else float(row[12]),
                                    }
                            else:
                                sale_order_line_values = {
                                        'order_id': self.order_id.id,
                                        'line_number':' ' if pd.isnull([row[0]]) else row[0],
                                        'product_id': product_id.id,
                                        'smart_account_mandatory':'' if pd.isnull([row[2]]) else row[2] ,
                                        'name': row[3],
                                        'cisco_product_ref':'' if pd.isnull([row[4]]) else row[4],
                                        'product_family': '' if pd.isnull([row[5]]) else row[5],
                                        'duration': 'N/A' if pd.isnull(row[6]) else row[6],
                                        'estimated_lead_time': 'N/A' if pd.isnull(row[7]) else row[7],
                                        'cost': 0 if pd.isnull(row[8]) else float(row[8]),
                                        'pricing_term': '' if pd.isnull([row[9]]) else row[9],
                                        'product_uom_qty': float(row[10]),
                                        'price_unit':float(row[11]), 
                                        'discount_metra': 0 if pd.isnull(row[12]) else float(row[12]),
                                    }    
                            sale_order_line = self.env['sale.order.line'].create(sale_order_line_values)  


                else:
                    if len(row) == 13:
                        if pd.isnull(row[1]):
                                    sale_order_line_values = {
                                        'order_id': self.order_id.id,
                                        'display_type': 'line_section',
                                        'name': row[0],
                                    
                                    }
                                    sale_order_line = self.env['sale.order.line'].create(sale_order_line_values)
                        else:            
                            if pd.isnull(row[10]):
                                list_price =0 if pd.isnull([row[7]]) else row[7]
                                dic_metra = 0 if pd.isnull([row[11]]) else row[11]
                                unit_price  = round(list_price - ((list_price * dic_metra) / 100), 2)
                            

                                sale_order_line_values = {
                                        'order_id': self.order_id.id,
                                        'line_number':' ' if pd.isnull([row[0]]) else row[0],
                                        'product_id': product_id.id,
                                        'smart_account_mandatory':'' if pd.isnull([row[2]]) else row[2] ,
                                        'name': row[3],
                                        'product_family': '' if pd.isnull([row[4]]) else row[4],
                                        'duration': 'N/A' if pd.isnull(row[5]) else row[5],
                                        'estimated_lead_time': 'N/A' if pd.isnull(row[6]) else row[6],
                                        'cost': 0 if pd.isnull(row[7]) else float(row[7]),
                                        'pricing_term': '' if pd.isnull([row[8]]) else row[8],
                                        'product_uom_qty': float(row[9]),
                                        'price_unit':unit_price, 
                                        'discount_metra': 0 if pd.isnull(row[11]) else float(row[11]),
                                    }
                            else:
                                sale_order_line_values = {
                                        'order_id': self.order_id.id,
                                        'line_number':' ' if pd.isnull([row[0]]) else row[0],
                                        'product_id': product_id.id,
                                        'smart_account_mandatory':'' if pd.isnull([row[2]]) else row[2] ,
                                        'name': row[3],
                                        'product_family': '' if pd.isnull([row[4]]) else row[4],
                                        'duration': 'N/A' if pd.isnull(row[5]) else row[5],
                                        'estimated_lead_time': 'N/A' if pd.isnull(row[6]) else row[6],
                                        'cost': 0 if pd.isnull(row[7]) else float(row[7]),
                                        'pricing_term': '' if pd.isnull([row[8]]) else row[8],
                                        'product_uom_qty': float(row[9]),
                                        'price_unit':float(row[10]), 
                                        'discount_metra': 0 if pd.isnull(row[11]) else float(row[11]),
                                    }
                            sale_order_line = self.env['sale.order.line'].create(sale_order_line_values)  
                    else:
                        raise ValidationError('The Number Of Columns More Than The Exsit Columns In The Lines')

                                 
        


        else:
            raise ValidationError('YOU DID NOT SELECT FILE TO IMPORT, PLEASE SELECT ONE')
         









          
                        
                          
        
            
        
            
    

       