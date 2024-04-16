from odoo import models, fields, api
import base64
import io
import pandas as pd
from odoo.exceptions import  ValidationError


class SaleOrderLinesImportWizard(models.TransientModel):
    _inherit = 'sale.order.lines.import.wizard'


    def action_import_sale_order_line(self):
        if self.order_lines_file:
            sale_order_line_data = base64.b64decode(self.order_lines_file)
            file_like_object = io.BytesIO(sale_order_line_data)
            data = pd.read_excel(file_like_object)
            df = pd.DataFrame(data)

            if self.order_id:
                line_id = self.env['sale.order.line'].search([('order_id', '=', self.order_id.id)])
                line_id.unlink()
            for index, row in df.iterrows():
                product_id = self.env['product.product'].search([('name', '=', row[1])])
                if not product_id:
                    product_id = self.env['product.product'].create({'name': row[1]})

                if len(row) == 20:
                    if pd.isnull(row[1]):
                        sale_order_line_values = {
                            'order_id': self.order_id.id,
                            'display_type': 'line_section',
                            'name': row[0],
                        
                        }
                        sale_order_line = self.env['sale.order.line'].create(sale_order_line_values) 
                    else:        
                        if pd.isnull(row[11]) or pd.isnull(row[14]) or pd.isnull(row[18]) or pd.isnull(row[19]):
                            unit_vendor_list_price =0 if pd.isnull([row[8]]) else float(row[8])
                            dic_metra = 0 if pd.isnull([row[12]]) else float(row[12])
                            qty= 0 if pd.isnull([row[10]]) else float(row[10])

                            unit_net_price  = round(unit_vendor_list_price - ((unit_vendor_list_price * dic_metra) / 100), 2)
                            total_price = round((unit_net_price * qty), 2)
                            partner_discount = 0 if pd.isnull([row[15]]) else float(row[15])
                            partner_unit_net_price  = round(unit_vendor_list_price - (unit_vendor_list_price * (partner_discount / 100)), 2)
                            margin= 0 if pd.isnull([row[16]]) else float(row[16])
                            conditions = 0 if pd.isnull([row[17]]) else float(row[17])
                            unit_selling_price  = (unit_net_price * (1+ conditions/100))/(1- margin/100)
                            total_selling_price = unit_selling_price * qty 

                                

                    
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
                                    'cost': unit_vendor_list_price,
                                    'pricing_term': '' if pd.isnull([row[9]]) else row[9],
                                    'product_uom_qty': qty,
                                    'unit_net_price':unit_net_price, 
                                    'discount_metra': dic_metra,
                                    'total_price': total_price,

                                    'partner_unit_net_price':partner_unit_net_price,
                                    'partner_discount': partner_discount,
                                    'mergin': margin,
                                    'conditions': conditions,

                                    'price_unit':unit_selling_price,
                                    'price_subtotal': total_selling_price,
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
                                    'unit_net_price':float(row[11]), 
                                    'discount_metra': 0 if pd.isnull(row[12]) else float(row[12]),
                                    'total_price': float(row[13]),
                                    'partner_unit_net_price': float(row[14]),
                                    'partner_discount': 0 if pd.isnull(row[15]) else float(row[15]),
                                    'mergin': 0 if pd.isnull(row[16]) else float(row[16]),
                                    'conditions': 0 if pd.isnull(row[17]) else float(row[17]),
                                    'price_unit':float(row[18]),
                                    'price_subtotal': float(row[19]),


                                }    
                        sale_order_line = self.env['sale.order.line'].create(sale_order_line_values)  
    
                else:
                    if pd.isnull(row[1]):
                        sale_order_line_values = {
                            'order_id': self.order_id.id,
                            'display_type': 'line_section',
                            'name': row[0],
                        
                        }
                        sale_order_line = self.env['sale.order.line'].create(sale_order_line_values) 
                    else:        
                            if pd.isnull(row[10]) or pd.isnull(row[13]) or pd.isnull(row[17]) or pd.isnull(row[18]):
                                unit_vendor_list_price =0 if pd.isnull([row[7]]) else float(row[7])
                                dic_metra = 0 if pd.isnull([row[11]]) else float(row[11])
                                qty= 0 if pd.isnull([row[9]]) else float(row[9])

                                unit_net_price  = round(unit_vendor_list_price - ((unit_vendor_list_price * dic_metra) / 100), 2)
                                total_price = round((unit_net_price * qty), 2)
                                partner_discount = 0 if pd.isnull([row[14]]) else float(row[14])
                                partner_unit_net_price  = round(unit_vendor_list_price - (unit_vendor_list_price * (partner_discount / 100)), 2)
                                margin= 0 if pd.isnull([row[15]]) else float(row[15])
                                conditions = 0 if pd.isnull([row[16]]) else float(row[16])
                                unit_selling_price  = (unit_net_price * (1+ conditions/100))/(1- margin/100)
                                total_selling_price = unit_selling_price * qty 

                                    

                        
                                sale_order_line_values = {
                                        'order_id': self.order_id.id,
                                        'line_number':' ' if pd.isnull([row[0]]) else row[0],
                                        'product_id': product_id.id,
                                        'smart_account_mandatory':'' if pd.isnull([row[2]]) else row[2] ,
                                        'name': row[3],
                                        'cisco_product_ref':'' if pd.isnull([row[4]]) else row[4],
                                        'product_family': '' if pd.isnull([row[5]]) else row[5],
                                        'estimated_lead_time': 'N/A' if pd.isnull(row[7]) else row[7],
                                        'cost': unit_vendor_list_price,
                                        'pricing_term': '' if pd.isnull([row[9]]) else row[9],
                                        'product_uom_qty': qty,
                                        'unit_net_price':unit_net_price, 
                                        'discount_metra': dic_metra,
                                        'total_price': total_price,

                                        'partner_unit_net_price':partner_unit_net_price,
                                        'partner_discount': partner_discount,
                                        'mergin': margin,
                                        'conditions': conditions,

                                        'price_unit':unit_selling_price,
                                        'price_subtotal': total_selling_price,
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
                                        'estimated_lead_time': 'N/A' if pd.isnull(row[6]) else row[6],
                                        'cost': 0 if pd.isnull(row[7]) else float(row[7]),
                                        'pricing_term': '' if pd.isnull([row[8]]) else row[8],
                                        'product_uom_qty': float(row[9]),
                                        'unit_net_price':float(row[10]), 
                                        'discount_metra': 0 if pd.isnull(row[11]) else float(row[11]),
                                        'total_price': float(row[12]),
                                        'partner_unit_net_price': float(row[13]),
                                        'partner_discount': 0 if pd.isnull(row[14]) else float(row[14]),
                                        'mergin': 0 if pd.isnull(row[15]) else float(row[15]),
                                        'conditions': 0 if pd.isnull(row[16]) else float(row[16]),
                                        'price_unit':float(row[17]),
                                        'price_subtotal': float(row[18]),


                                    }    
                            sale_order_line = self.env['sale.order.line'].create(sale_order_line_values)  
            
                    

    
              


                 
                  

                                 
        


        else:
            raise ValidationError('YOU DID NOT SELECT FILE TO IMPORT, PLEASE SELECT ONE')