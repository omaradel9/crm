from odoo import models, fields, api
import base64
import io
import pandas as pd
from odoo.exceptions import  ValidationError


class SaleOrderLinesImportWizard(models.TransientModel):
    _inherit = 'sale.order.lines.import.wizard'

   

    


    def check_values(self,value,label):

        if isinstance(value, str):
            raise ValidationError("Invalid value for %s"% label)
        else:
            num = float(value)

        return num  
    # def insert_lines_without_durtaion(self, df):
    #     for index, row in df.iterrows():
    #         product_id = self.env['product.product'].search([('name', '=', row[1])])
    #         if not product_id:
    #             product_id = self.env['product.product'].create({'name': row[1]})
    #         if pd.isnull(row[1]):
    #             sale_order_line_values = {
    #                 'order_id': self.order_id.id,
    #                 'display_type': 'line_section',
    #                 'name': row[0],
                
    #             }
    #             sale_order_line = self.env['sale.order.line'].create(sale_order_line_values) 
    #         else:        
    #             if pd.isnull(row[10]) or row[10] == 0 or pd.isnull(row[12]) or row[12] == 0 or pd.isnull(row[13]) or row[13] == 0 or pd.isnull(row[17]) or row[17] == 0 or pd.isnull(row[18]) or row[18] == 0:
    #                 unit_vendor_list_price =0 if pd.isnull([row[7]]) else self.check_values(row[7], 'Unit Vendor List Price')
    #                 dic_metra = 0 if pd.isnull([row[11]]) else self.check_values(row[11], 'Vendor Discount')
    #                 qty= 0 if pd.isnull([row[9]]) else self.check_values(row[9],'Quantity')

    #                 unit_net_price  = round(unit_vendor_list_price - ((unit_vendor_list_price * dic_metra) / 100), 2)
    #                 total_price = round((unit_net_price * qty), 2)
    #                 partner_discount = 0 if pd.isnull([row[14]]) else self.check_values(row[14], 'Partner Discount')
    #                 partner_unit_net_price  = round(unit_vendor_list_price - (unit_vendor_list_price * (partner_discount / 100)), 2)
    #                 margin= 0 if pd.isnull([row[16]]) else self.check_values(row[16], 'Margin')
    #                 conditions = 0 if pd.isnull([row[15]]) else  self.check_values(row[15], 'Conditions')
    #                 unit_selling_price  = (unit_net_price * (1+ conditions/100))/(1- margin/100)
    #                 total_selling_price = unit_selling_price * qty 

                        

            
    #                 sale_order_line_values = {
    #                         'order_id': self.order_id.id,
    #                         'line_number':' ' if pd.isnull([row[0]]) else row[0],
    #                         'product_id': product_id.id,
    #                         'smart_account_mandatory':'' if pd.isnull([row[2]]) else row[2] ,
    #                         'name': row[3],
    #                         'cisco_product_ref':'' if pd.isnull([row[4]]) else row[4],
    #                         'product_family': '' if pd.isnull([row[5]]) else row[5],
    #                         'estimated_lead_time': 'N/A' if pd.isnull(row[7]) else row[7],
    #                         'cost': unit_vendor_list_price,
    #                         'pricing_term': '' if pd.isnull([row[9]]) else row[9],
    #                         'product_uom_qty': qty,
    #                         'unit_net_price':unit_net_price, 
    #                         'discount_metra': dic_metra,
    #                         'total_price': total_price,

    #                         'partner_unit_net_price':partner_unit_net_price,
    #                         'partner_discount': partner_discount,
    #                         'mergin': margin,
    #                         'conditions': conditions,

    #                         'price_unit':unit_selling_price,
    #                         'price_subtotal': total_selling_price,
    #                     }
    #             else:
    #                 sale_order_line_values = {
    #                         'order_id': self.order_id.id,
    #                         'line_number':' ' if pd.isnull([row[0]]) else row[0],
    #                         'product_id': product_id.id,
    #                         'smart_account_mandatory':'' if pd.isnull([row[2]]) else row[2] ,
    #                         'name': row[3],
    #                         'cisco_product_ref':'' if pd.isnull([row[4]]) else row[4],
    #                         'product_family': '' if pd.isnull([row[5]]) else row[5],
    #                         'estimated_lead_time': 'N/A' if pd.isnull(row[6]) else row[6],
    #                         'cost': 0 if pd.isnull(row[7]) else self.check_values(row[7], 'Unit Vendor List Price'),
    #                         'pricing_term': '' if pd.isnull([row[8]]) else row[8],
    #                         'product_uom_qty': float(row[9]),
    #                         'unit_net_price':float(row[10]), 
    #                         'discount_metra': 0 if pd.isnull(row[11]) else self.check_values(row[11], 'Vendor Discount'),
    #                         'total_price': float(row[12]),
    #                         'partner_unit_net_price': float(row[13]),
    #                         'partner_discount': 0 if pd.isnull(row[14]) else self.check_values(row[14], 'Partner Discount'),
    #                         'mergin': 0 if pd.isnull(row[16]) else self.check_values(row[16], 'Margin'),
    #                         'conditions': 0 if pd.isnull(row[15]) else self.check_values(row[15], 'Conditions'),
    #                         'price_unit':self.check_values(row[17], 'Unit Selling Price'),
    #                         'price_subtotal':self.check_values(row[18], 'Total Selling Price'),


    #                     }    
    #             sale_order_line = self.env['sale.order.line'].create(sale_order_line_values)  

    def insert_lines_with_duration(self,df):
        for index, row in df.iterrows():
            product_id = self.env['product.product'].search([('name', '=', row[1])])
            if not product_id:
                product_id = self.env['product.product'].create({'name': row[1]})

            if len(row) == 20:
                print('-------------------------fffffffffffffffffffffff')

                if pd.isnull(row[1]):
                    sale_order_line_values = {
                        'order_id': self.order_id.id,
                        'display_type': 'line_section',
                        'name': row[0],
                    
                    }
                    sale_order_line = self.env['sale.order.line'].create(sale_order_line_values) 
                else:        
                    if pd.isnull(row[11]) or row[11] == 0 or pd.isnull(row[14]) or row[14] == 0 or pd.isnull(row[18]) or row[18] == 0 or pd.isnull(row[19]) or row[19] == 0:
                        unit_vendor_list_price =0 if pd.isnull([row[8]]) else self.check_values(row[8], 'Unit Vendor List Price')
                        dic_metra = 0 if pd.isnull([row[12]]) else self.check_values(row[12], 'Vendor Discount')
                        qty= 0 if pd.isnull([row[10]]) else self.check_values(row[10],'Quantity')

                        unit_net_price  = round(unit_vendor_list_price - ((unit_vendor_list_price * dic_metra) / 100), 2)
                        total_price = round((unit_net_price * qty), 2)
                        partner_discount = 0 if pd.isnull([row[15]]) else self.check_values(row[15], 'Partner Discount')
                        partner_unit_net_price  = round(unit_vendor_list_price - (unit_vendor_list_price * (partner_discount / 100)), 2)
                        margin= 0 if pd.isnull([row[17]]) else self.check_values(row[17], 'Margin')
                        conditions = 0 if pd.isnull([row[16]]) else self.check_values(row[16], 'Conditions')
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
                                'cost': 0 if pd.isnull(row[8]) else self.check_values(row[8], 'Unit Vendor List Price'),
                                'pricing_term': '' if pd.isnull([row[9]]) else row[9],
                                'product_uom_qty': self.check_values(row[10],'Quantity'),
                                'unit_net_price':self.check_values(row[11], 'Unit Net Price'), 
                                'discount_metra': 0 if pd.isnull(row[12]) else self.check_values(row[12], 'Vendor Discount'),
                                'total_price':self.check_values(row[13], 'Total Price'),
                                'partner_unit_net_price': self.check_values(row[14], 'Partner Unit Net Price'),
                                'partner_discount': 0 if pd.isnull(row[15]) else self.check_values(row[15], 'Partner Discount'),
                                'mergin': 0 if pd.isnull(row[17]) else self.check_values(row[17], 'Margin'),
                                'conditions': 0 if pd.isnull(row[16]) else self.check_values(row[16], 'Conditions'),
                                'price_unit':self.check_values(row[18], 'Unit Selling Price'),
                                'price_subtotal': self.check_values(row[19], 'Total Selling Price'),


                            }    
                    sale_order_line = self.env['sale.order.line'].create(sale_order_line_values)

            else:
                # self.insert_lines_without_durtaion(df)
                raise ValidationError('There is a missing column in your file')        


    def action_import_sale_order_line(self):
        if self.order_lines_file:
            sale_order_line_data = base64.b64decode(self.order_lines_file)
            file_like_object = io.BytesIO(sale_order_line_data)
            data = pd.read_excel(file_like_object)
            df = pd.DataFrame(data)
            if self.order_id:
                line_id = self.env['sale.order.line'].search([('order_id', '=', self.order_id.id)])
                if self.import_lines_types == 'update_lines':
                    line_id.unlink()
                    self.insert_lines_with_duration(df)
                elif self.import_lines_types == 'add_lines':
                    self.insert_lines_with_duration(df)
                else:
                    raise ValidationError('You need to select value from the Import Type Field')    



                 
                  

                                 
        


        else:
            raise ValidationError('YOU DID NOT SELECT FILE TO IMPORT, PLEASE SELECT ONE')                            





    # def action_import_sale_order_line(self):
    #     if self.order_lines_file:
    #         sale_order_line_data = base64.b64decode(self.order_lines_file)
    #         file_like_object = io.BytesIO(sale_order_line_data)
    #         data = pd.read_excel(file_like_object)
    #         df = pd.DataFrame(data)

    #         if self.order_id:
    #             line_id = self.env['sale.order.line'].search([('order_id', '=', self.order_id.id)])

    #             if self.order_id.import_lines_type == 'update_lines':
    #                 line_id.unlink()
    #                 for index, row in df.iterrows():
    #                     product_id = self.env['product.product'].search([('name', '=', row[1])])
    #                     if not product_id:
    #                         product_id = self.env['product.product'].create({'name': row[1]})

    #                     if len(row) == 20:
    #                         if pd.isnull(row[1]):
    #                             sale_order_line_values = {
    #                                 'order_id': self.order_id.id,
    #                                 'display_type': 'line_section',
    #                                 'name': row[0],
                                
    #                             }
    #                             sale_order_line = self.env['sale.order.line'].create(sale_order_line_values) 
    #                         else:        
    #                             if pd.isnull(row[11]) or row[11] == 0 or pd.isnull(row[14]) or row[14] == 0 or pd.isnull(row[18]) or row[18] == 0 or pd.isnull(row[19]) or row[19] == 0:
    #                                 unit_vendor_list_price =0 if pd.isnull([row[8]]) else self.check_values(row[8], 'Unit Vendor List Price')
    #                                 dic_metra = 0 if pd.isnull([row[12]]) else self.check_values(row[12], 'Vendor Discount')
    #                                 qty= 0 if pd.isnull([row[10]]) else self.check_values(row[10],'Quantity')

    #                                 unit_net_price  = round(unit_vendor_list_price - ((unit_vendor_list_price * dic_metra) / 100), 2)
    #                                 total_price = round((unit_net_price * qty), 2)
    #                                 partner_discount = 0 if pd.isnull([row[15]]) else self.check_values(row[15], 'Partner Discount')
    #                                 partner_unit_net_price  = round(unit_vendor_list_price - (unit_vendor_list_price * (partner_discount / 100)), 2)
    #                                 margin= 0 if pd.isnull([row[17]]) else self.check_values(row[17], 'Margin')
    #                                 conditions = 0 if pd.isnull([row[16]]) else self.check_values(row[16], 'Conditions')
    #                                 unit_selling_price  = (unit_net_price * (1+ conditions/100))/(1- margin/100)
    #                                 total_selling_price = unit_selling_price * qty 

                                        

                            
    #                                 sale_order_line_values = {
    #                                         'order_id': self.order_id.id,
    #                                         'line_number':' ' if pd.isnull([row[0]]) else row[0],
    #                                         'product_id': product_id.id,
    #                                         'smart_account_mandatory':'' if pd.isnull([row[2]]) else row[2] ,
    #                                         'name': row[3],
    #                                         'cisco_product_ref':'' if pd.isnull([row[4]]) else row[4],
    #                                         'product_family': '' if pd.isnull([row[5]]) else row[5],
    #                                         'duration': 'N/A' if pd.isnull(row[6]) else row[6],
    #                                         'estimated_lead_time': 'N/A' if pd.isnull(row[7]) else row[7],
    #                                         'cost': unit_vendor_list_price,
    #                                         'pricing_term': '' if pd.isnull([row[9]]) else row[9],
    #                                         'product_uom_qty': qty,
    #                                         'unit_net_price':unit_net_price, 
    #                                         'discount_metra': dic_metra,
    #                                         'total_price': total_price,

    #                                         'partner_unit_net_price':partner_unit_net_price,
    #                                         'partner_discount': partner_discount,
    #                                         'mergin': margin,
    #                                         'conditions': conditions,

    #                                         'price_unit':unit_selling_price,
    #                                         'price_subtotal': total_selling_price,
    #                                     }
    #                             else:
    #                                 sale_order_line_values = {
    #                                         'order_id': self.order_id.id,
    #                                         'line_number':' ' if pd.isnull([row[0]]) else row[0],
    #                                         'product_id': product_id.id,
    #                                         'smart_account_mandatory':'' if pd.isnull([row[2]]) else row[2] ,
    #                                         'name': row[3],
    #                                         'cisco_product_ref':'' if pd.isnull([row[4]]) else row[4],
    #                                         'product_family': '' if pd.isnull([row[5]]) else row[5],
    #                                         'duration': 'N/A' if pd.isnull(row[6]) else row[6],
    #                                         'estimated_lead_time': 'N/A' if pd.isnull(row[7]) else row[7],
    #                                         'cost': 0 if pd.isnull(row[8]) else self.check_values(row[8], 'Unit Vendor List Price'),
    #                                         'pricing_term': '' if pd.isnull([row[9]]) else row[9],
    #                                         'product_uom_qty': self.check_values(row[10],'Quantity'),
    #                                         'unit_net_price':self.check_values(row[11], 'Unit Net Price'), 
    #                                         'discount_metra': 0 if pd.isnull(row[12]) else self.check_values(row[12], 'Vendor Discount'),
    #                                         'total_price':self.check_values(row[13], 'Total Price'),
    #                                         'partner_unit_net_price': self.check_values(row[14], 'Partner Unit Net Price'),
    #                                         'partner_discount': 0 if pd.isnull(row[15]) else self.check_values(row[15], 'Partner Discount'),
    #                                         'mergin': 0 if pd.isnull(row[17]) else self.check_values(row[17], 'Margin'),
    #                                         'conditions': 0 if pd.isnull(row[16]) else self.check_values(row[16], 'Conditions'),
    #                                         'price_unit':self.check_values(row[18], 'Unit Selling Price'),
    #                                         'price_subtotal': self.check_values(row[19], 'Total Selling Price'),


    #                                     }    
    #                             sale_order_line = self.env['sale.order.line'].create(sale_order_line_values)  
            
    #                     else:
    #                         if pd.isnull(row[1]):
    #                             sale_order_line_values = {
    #                                 'order_id': self.order_id.id,
    #                                 'display_type': 'line_section',
    #                                 'name': row[0],
                                
    #                             }
    #                             sale_order_line = self.env['sale.order.line'].create(sale_order_line_values) 
    #                         else:        
    #                                 if pd.isnull(row[10]) or row[10] == 0 or pd.isnull(row[12]) or row[12] == 0 or pd.isnull(row[13]) or row[13] == 0 or pd.isnull(row[17]) or row[17] == 0 or pd.isnull(row[18]) or row[18] == 0:
    #                                     unit_vendor_list_price =0 if pd.isnull([row[7]]) else self.check_values(row[7], 'Unit Vendor List Price')
    #                                     dic_metra = 0 if pd.isnull([row[11]]) else self.check_values(row[11], 'Vendor Discount')
    #                                     qty= 0 if pd.isnull([row[9]]) else self.check_values(row[9],'Quantity')

    #                                     unit_net_price  = round(unit_vendor_list_price - ((unit_vendor_list_price * dic_metra) / 100), 2)
    #                                     total_price = round((unit_net_price * qty), 2)
    #                                     partner_discount = 0 if pd.isnull([row[14]]) else self.check_values(row[14], 'Partner Discount')
    #                                     partner_unit_net_price  = round(unit_vendor_list_price - (unit_vendor_list_price * (partner_discount / 100)), 2)
    #                                     margin= 0 if pd.isnull([row[16]]) else self.check_values(row[16], 'Margin')
    #                                     conditions = 0 if pd.isnull([row[15]]) else  self.check_values(row[15], 'Conditions')
    #                                     unit_selling_price  = (unit_net_price * (1+ conditions/100))/(1- margin/100)
    #                                     total_selling_price = unit_selling_price * qty 

                                            

                                
    #                                     sale_order_line_values = {
    #                                             'order_id': self.order_id.id,
    #                                             'line_number':' ' if pd.isnull([row[0]]) else row[0],
    #                                             'product_id': product_id.id,
    #                                             'smart_account_mandatory':'' if pd.isnull([row[2]]) else row[2] ,
    #                                             'name': row[3],
    #                                             'cisco_product_ref':'' if pd.isnull([row[4]]) else row[4],
    #                                             'product_family': '' if pd.isnull([row[5]]) else row[5],
    #                                             'estimated_lead_time': 'N/A' if pd.isnull(row[7]) else row[7],
    #                                             'cost': unit_vendor_list_price,
    #                                             'pricing_term': '' if pd.isnull([row[9]]) else row[9],
    #                                             'product_uom_qty': qty,
    #                                             'unit_net_price':unit_net_price, 
    #                                             'discount_metra': dic_metra,
    #                                             'total_price': total_price,

    #                                             'partner_unit_net_price':partner_unit_net_price,
    #                                             'partner_discount': partner_discount,
    #                                             'mergin': margin,
    #                                             'conditions': conditions,

    #                                             'price_unit':unit_selling_price,
    #                                             'price_subtotal': total_selling_price,
    #                                         }
    #                                 else:
    #                                     sale_order_line_values = {
    #                                             'order_id': self.order_id.id,
    #                                             'line_number':' ' if pd.isnull([row[0]]) else row[0],
    #                                             'product_id': product_id.id,
    #                                             'smart_account_mandatory':'' if pd.isnull([row[2]]) else row[2] ,
    #                                             'name': row[3],
    #                                             'cisco_product_ref':'' if pd.isnull([row[4]]) else row[4],
    #                                             'product_family': '' if pd.isnull([row[5]]) else row[5],
    #                                             'estimated_lead_time': 'N/A' if pd.isnull(row[6]) else row[6],
    #                                             'cost': 0 if pd.isnull(row[7]) else self.check_values(row[7], 'Unit Vendor List Price'),
    #                                             'pricing_term': '' if pd.isnull([row[8]]) else row[8],
    #                                             'product_uom_qty': float(row[9]),
    #                                             'unit_net_price':float(row[10]), 
    #                                             'discount_metra': 0 if pd.isnull(row[11]) else self.check_values(row[11], 'Vendor Discount'),
    #                                             'total_price': float(row[12]),
    #                                             'partner_unit_net_price': float(row[13]),
    #                                             'partner_discount': 0 if pd.isnull(row[14]) else self.check_values(row[14], 'Partner Discount'),
    #                                             'mergin': 0 if pd.isnull(row[16]) else self.check_values(row[16], 'Margin'),
    #                                             'conditions': 0 if pd.isnull(row[15]) else self.check_values(row[15], 'Conditions'),
    #                                             'price_unit':self.check_values(row[17], 'Unit Selling Price'),
    #                                             'price_subtotal':self.check_values(row[18], 'Total Selling Price'),


    #                                         }    
    #                                 sale_order_line = self.env['sale.order.line'].create(sale_order_line_values)  
            
    #             else:


                 
                  

                                 
        


    #     else:
    #         raise ValidationError('YOU DID NOT SELECT FILE TO IMPORT, PLEASE SELECT ONE')