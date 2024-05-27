from odoo import models, fields, api
import base64
import io
import pandas as pd
from odoo.exceptions import  ValidationError


class SaleOrderLinesImportWizard(models.TransientModel):
    _inherit = 'sale.order.lines.import.wizard'

   

    


  

    def insert_lines_with_duration(self,df):
        for index, row in df.iterrows():
            product_id = self.env['product.product'].search([('name', '=', row[1])])
            if not product_id:
                product_id = self.env['product.product'].create({'name': row[1],'description_sale': row[3]})

            if len(row) == 25:

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

                        qty= 0 if pd.isnull([row[10]])  else self.check_values(row[10],'Quantity')

                   
                        total_price = 0 if pd.isnull([row[13]]) else self.check_values(row[13], 'Total Price')
                        if qty != 0:
                            unit_net_price  = round(total_price/qty,2)
                        else:
                            unit_net_price = 0

                        partner_discount = 0 if pd.isnull([row[15]]) else self.check_values(row[15], 'Partner Discount')
                        partner_unit_net_price  = round(unit_net_price - (unit_net_price * (partner_discount / 100)), 2)
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

                                'product_number':'' if pd.isnull([row[20]]) else row[20],
                                'last_date_of_support': '' if pd.isnull([row[21]]) else row[21],
                                'serial_number': '' if pd.isnull([row[22]]) else row[22],
                                'start_date': '' if pd.isnull([row[23]]) else row[23],

                                'end_date':'' if pd.isnull([row[24]]) else row[24],
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

                                'product_number':'' if pd.isnull([row[20]]) else row[20],
                                'last_date_of_support': '' if pd.isnull([row[21]]) else row[21],
                                'serial_number': '' if pd.isnull([row[22]]) else row[22],
                                'start_date': '' if pd.isnull([row[23]]) else row[23],

                                'end_date':'' if pd.isnull([row[24]]) else row[24],


                            }    
                    sale_order_line = self.env['sale.order.line'].create(sale_order_line_values)

            else:
                raise ValidationError('There is a missing column in your file') 