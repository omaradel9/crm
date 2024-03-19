
from odoo import  models, _
import base64
import io
from odoo.modules.module import get_module_resource
from bs4 import BeautifulSoup
from num2words import num2words



class QuotationReportXlsx(models.AbstractModel):
    _inherit= 'report.sale_order_reports.custom_sale_order_action_report_xlsx'







    def generate_xlsx_report(self, workbook, data, orders):
        format_1 = workbook.add_format({'bold':True,'align': 'center','bg_color':'gray','font_size':14})
        format_2 = workbook.add_format({'bold':True,'align': 'center','bg_color':'gray','font_size':12,})
        format_3 = workbook.add_format({'bold':True,'font_size':12,'underline':True})
        format_4 = workbook.add_format({'bold':True,'font_size':11,'text_wrap': True})
        format_5 = workbook.add_format({'font_size':11,'text_wrap': True})



        bold = workbook.add_format({'bold':True,'font_size': 12,'text_wrap': True,'border_color': 'red'})
        center =  workbook.add_format({'align':'center'})
        currency = workbook.add_format({'num_format': orders.currency_id.symbol + '#,##0.00','align':'right'})
        white_bg = workbook.add_format ({'bg_color':'white'}) 
        border_top = workbook.add_format ({'top':True})
        border_bottom = workbook.add_format ({'bottom':True})
        left_border = workbook.add_format({'left':True}) 
        right_border = workbook.add_format({'right':False})
        qt_border = workbook.add_format({'bottom':True,'top':True})
        table_border = workbook.add_format({'bottom':True,'top':True,'right':True,'left':True})

         

        date_format = workbook.add_format({'text_wrap': True, 'num_format': 'yyyy-mm-dd','align': 'left',}) 
        
    
        sheet = workbook.add_worksheet('Sale Order Summary')
        sheet.set_column(3, 3, 20)
        sheet.set_column(1, 1, 20)
        sheet.set_column(6, 6, 20)
        sheet.set_column(8, 8, 20)
        sheet.set_column(7, 7, 40)
        sheet.set_column(5, 5, 20)

       
      
        sheet.merge_range(6, 0 , 6 ,8,'Quotation',format_1)
        sheet.conditional_format(f'A1:I6',{'type':'formula','criteria': True,'format':white_bg}) 

        sheet.conditional_format(f'A7:I7',{'type':'formula','criteria': True,'format':qt_border}) 
         
        sheet.conditional_format(f'A8:I12',{'type':'formula','criteria': True,'format':white_bg})
        
        sheet.conditional_format(f'A12:I12',{'type':'formula','criteria': True,'format':border_top})

        sheet.conditional_format(f'A12:I13',{'type':'formula','criteria': True,'format':white_bg}) 
 

 
        row = 6
        table_row = 14
      
        for obj in orders:
            sheet.insert_image(0,1, get_module_resource('sale_order_reports', 'static/src/img', 'metra.png'))

            if obj.brand_id.image:
                brand_image = io.BytesIO(base64.b64decode(obj.brand_id.image))
                sheet.insert_image(0,8,"image.png",{'image_data':brand_image,'x_scale':0.5,'y_scale':0.4})


            row +=1
            sheet.merge_range(row, 0 ,row,2,'Partner name:',bold)
            sheet.write(row, 3,obj.partner_id.name)
            sheet.merge_range(row, 5 ,row,6,'Sales Person:',bold)
            sheet.write(row, 7,obj.user_id.name)
            row += 1 
            sheet.merge_range(row, 0 ,row,2,'Quotation Date:',bold)
            sheet.write(row, 3,obj.date_order, date_format)
            sheet.merge_range(row, 5 ,row,6,'Sales Person Mail:',bold)
            sheet.write(row, 7,obj.user_id.email)
            row += 1 
            sheet.merge_range(row, 0 ,row,2,'Expiration Date:',bold)
            sheet.write(row, 3,obj.validity_date,date_format)
            sheet.merge_range(row, 5 ,row,6,'Sales Phone:',bold)
            sheet.write(row, 7,obj.user_id.phone or "")
            row += 1 
            sheet.merge_range(row, 0 ,row,2,'End User:',bold)
            sheet.write(row, 3,obj.end_user_id.name or "")
            row += 1 
            
            bold_static = workbook.add_format({'bold':True,'font_size': 9,'text_wrap': True})
            sheet.merge_range(row, 0 ,row,8,'We will be happy to supply any further information you may need and trust that your call on us to fill your order, which will receive our prompt and careful attention.',bold_static)
            row += 1
            sheet.merge_range(row, 0 ,row,8,'We are pleased to quote you the following:',bold_static)

            sheet.write(13,0,'Items',format_2)    
            sheet.write(13,1,'Part Number',format_2)    
            sheet.merge_range(13, 2 ,13,4,'Product Description',format_2)
  
            sheet.write(13,5,'Duration (Months)',format_2)    
            sheet.write(13,6,'Quantity',format_2)    
            sheet.write(13,7,'Unite Price',format_2)    
            sheet.write(13,8,'Total price',format_2) 

            section_format = workbook.add_format({'bold':True,'font_size': 11,'text_wrap': True})



            index = 1
            for product in obj.order_line:
                # vat_percentage = str(int(product.tax_id.amount)) + "%"
                if product.display_type == 'line_section':
                    sheet.merge_range(table_row, 0, table_row, 8, product.name or "",section_format)
                elif product.display_type == 'line_note':
                    sheet.merge_range(table_row, 0, table_row, 8, product.name or "",section_format)
                else:
                    sheet.write(table_row, 0, product.line_number or index, center)
                    sheet.write(table_row, 1, product.product_template_id.name or "")
                    sheet.merge_range(table_row, 2, table_row, 4, product.name or "")
                    sheet.write(table_row, 5, product.duration or "N/A", center)
                    sheet.write(table_row, 6, product.product_uom_qty or "", center)
                    sheet.write(table_row, 7, product.price_unit or "", currency)
                    sheet.write(table_row, 8, product.price_subtotal or "", currency)
                table_row += 1
                

               
                index +=1

            sheet.merge_range(table_row,0,table_row,7,'Sub Totals In USD Excluding VAT',format_2)
            sheet.write(table_row, 8,obj.amount_untaxed or "", currency)

            table_row += 1
            if obj.term_conditions_id.tax:
                    vat_str = f'Value-Added Tax (VAT) ({obj.term_conditions_id.tax})'
            else:
                    vat_str = f'Value-Added Tax (VAT) (0)'
         
            sheet.merge_range(table_row,0,table_row,7,vat_str,format_2) 
            sheet.write(table_row, 8,obj.amount_tax or "", currency)
           
            table_row += 1
            
            
            sheet.merge_range(table_row,0,table_row,7,'Total Prices In USD Including VAT',format_2)  
            sheet.write(table_row, 8,obj.amount_total or "", currency) 

            table_row += 1
            sheet.conditional_format(f"A14:I{table_row}",{'type':'formula','criteria': True,'format':table_border})
            sheet.conditional_format(f"J14:J{table_row}",{'type':'formula','criteria': True,'format':left_border})




            sheet.conditional_format(f"A{table_row}:I{table_row+21}",{'type':'formula','criteria': True,'format':white_bg})

            table_row +=1
            if obj.pricelist_id.currency_id:
                sheet.set_row(table_row,30)
                sheet.merge_range(table_row, 0, table_row, 2, 'Currency:', format_4)
                sheet.merge_range(table_row, 3, table_row, 8, obj.pricelist_id.currency_id.name, format_4)
                table_row += 2
            # if obj.pricelist_id.currency_id:
            #     sheet.set_row(table_row,30)
            #     sheet.merge_range(table_row, 0, table_row, 2, 'Currency:', format_4)
            #     sheet.merge_range(table_row, 3, table_row, 8, obj.pricelist_id.currency_id.name, format_4)
            #     table_row += 2   
            if  obj.amount_total:
                sheet.set_row(table_row,30) 
                sheet.merge_range(table_row, 0, table_row, 2, 'Total in Word:', format_4)
                sheet.merge_range(table_row, 3, table_row, 8, num2words(obj.amount_total).upper(), format_4)

                table_row += 2
            if obj.payment_term_id:
                sheet.set_row(table_row,30)
                soup = BeautifulSoup(obj.payment_term_id.note, 'html.parser')
                payment = soup.get_text()  
                sheet.merge_range(table_row, 0, table_row, 2, 'Payment Terms:', format_4)
                sheet.merge_range(table_row, 3, table_row, 8, payment, format_4)
                table_row += 2
            if obj.payment_method:
                sheet.set_row(table_row,30) 
                sheet.merge_range(table_row, 0, table_row, 2, 'Payment Method:', format_4)
                sheet.merge_range(table_row, 3, table_row, 8, obj.payment_method, format_4)
                table_row += 2
            if obj.incoterms:
                sheet.set_row(table_row,30)  
                sheet.merge_range(table_row, 0, table_row, 2, 'Incoterms:', format_4)
                sheet.merge_range(table_row, 3, table_row, 8, obj.incoterms, format_4)
                table_row += 2
            if obj.delivery_location:
                sheet.set_row(table_row,30)   
                sheet.merge_range(table_row, 0, table_row, 2, 'Delivery Location:', format_4)
                sheet.merge_range(table_row, 3, table_row, 8, obj.delivery_location, format_4)
                table_row += 2
            if obj.mode_of_shipment:
                sheet.set_row(table_row,30)
                sheet.merge_range(table_row, 0, table_row, 2, 'Mode of Shipment:', format_4)
                sheet.merge_range(table_row, 3, table_row, 8, obj.mode_of_shipment, format_4)
                sheet.set_row(table_row, None, None, {'level': 1, 'hidden': False, 'collapsed': False, 'autofit': True})

                table_row += 2
            if obj.end_user_id:
                sheet.set_row(table_row,30)   
                sheet.merge_range(table_row, 0, table_row, 2, 'End Customer:', format_4)
                sheet.merge_range(table_row, 3, table_row, 8, obj.end_user_id.name, format_4)
                table_row += 5
            text_one = '''These commodities, technology or software were exported in accordance with the US Export Administration Regulations. Diversion contrary to U.S. law prohibited. The
purchaser agrees to indemnify the seller and hold the seller harmless from and against all claims, liability, and obligation whatsoever (including, but not limited to, reasonable
attorneys' fees) arising out of the transfer of these commodities across national boundaries without proper government licenses and authorizations. Reexport/retransfer
without prior authorization from the US Bureau of Export Administration is prohibited. Export, reexport, sale or retransfer to military end-users or end-uses in prohibited
destinations and proliferation end-users and end-uses is strictly prohibited without prior authorization from the US government.'''  
            text_two = '''
You agree that you have reviewed the Metra Standard terms and conditions of sale and that your purchase is subject to these T's and C's.
'''          
            text_three = '''
This document is Metra's system generated Document and does not require anyone signature nor Metra's stamp on it.
'''
            sheet.merge_range(table_row, 0, table_row, 8,text_one, format_5)
            table_row += 2 


            sheet.merge_range(table_row, 0, table_row, 8,text_two, format_5)
            table_row += 2

            sheet.merge_range(table_row, 0, table_row, 8,text_three, format_5)
       