
from odoo import  models, _
import base64
import io
from odoo.modules.module import get_module_resource
from bs4 import BeautifulSoup
from num2words import num2words



class QuotationReportXlsx(models.AbstractModel):
    _inherit= 'report.sale_order_reports.custom_sale_order_action_report_xlsx'







    def generate_xlsx_report(self, workbook, data, orders):
        format_1 = workbook.add_format({'bold':True,'align': 'center','bg_color':'#D3D3D3','font_size':14})
        format_2 = workbook.add_format({'bold':True,'align': 'center','bg_color':'#D3D3D3','font_size':12,})
        # format_3 = workbook.add_format({'bold':True,'font_size':12,'underline':True})
        format_3 = workbook.add_format({'bold':True,'align': 'left','bg_color':'#D3D3D3','font_size':12,})

        format_4 = workbook.add_format({'bold':True,'font_size':11,'text_wrap': True})
        format_5 = workbook.add_format({'font_size':11,'text_wrap': True})
        format_6 = workbook.add_format({'bold':True,'font_size':11,'text_wrap': True})



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
            sheet.insert_image(2,1, get_module_resource('sale_order_reports', 'static/src/img', 'Metra_logo_navy_RGB.png'),{'x_scale': 0.2, 'y_scale': 0.2})

            if obj.brand_id.image:
                brand_image = io.BytesIO(base64.b64decode(obj.brand_id.image))
                sheet.insert_image(2,8,"image.png",{'image_data':brand_image,'x_scale':0.5,'y_scale':0.4})


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

            sheet.merge_range(table_row,0,table_row,7,'Sub Totals In USD Excluding VAT',format_3)
            sheet.write(table_row, 8,obj.amount_untaxed or "", currency)

            table_row += 1
            if obj.term_conditions_id.tax:
                    vat_str = f'Value-Added Tax (VAT) ({obj.term_conditions_id.tax})'
            else:
                    vat_str = f'Value-Added Tax (VAT) (0)'
         
            sheet.merge_range(table_row,0,table_row,7,vat_str,format_3) 
            sheet.write(table_row, 8,obj.amount_tax or "", currency)
           
            table_row += 1
            
            
            sheet.merge_range(table_row,0,table_row,7,'Total Prices In USD Including VAT',format_3)  
            sheet.write(table_row, 8,obj.amount_total or "", currency) 

            table_row += 1
            sheet.conditional_format(f"A14:I{table_row}",{'type':'formula','criteria': True,'format':table_border})
            sheet.conditional_format(f"J14:J{table_row}",{'type':'formula','criteria': True,'format':left_border})




            sheet.conditional_format(f"A{table_row}:I{table_row+55}",{'type':'formula','criteria': True,'format':white_bg})

            table_row +=1
            if obj.pricelist_id.currency_id:
                sheet.set_row(table_row,30)
                sheet.merge_range(table_row, 0, table_row, 2, 'Currency:', format_4)
                sheet.merge_range(table_row, 3, table_row, 8, obj.pricelist_id.currency_id.name, format_4)
                table_row += 2
            if obj.brand_id:
                sheet.set_row(table_row,30)
                sheet.merge_range(table_row, 0, table_row, 2, 'Usage:', format_4)
                sheet.merge_range(table_row, 3, table_row, 8, obj.brand_id.name, format_4)
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
            table_row += 2



            sheet.merge_range(table_row, 0, table_row, 8,'Terms and Conditions', format_6)
            table_row += 1

            sheet.merge_range(table_row, 0, table_row, 8,'Metra Computer Group', format_6)
            table_row += 3
            text_term_one='''Quotations are only valid in writing and during the period that they state. If unstated, the period is 3 days. Please check the
Order Confirmation and notify Metra of any mistake in writing immediately or the details stated in the Order confirmation
will apply to this Agreement. All product and pricing information is based on latest information available. Subject to change
without notice or obligation. The customer cannot cancel or change a Purchase Orders or Order Confirmation sent to Metra.
The customer/s are obliged to accept the deliveries within (2) calendar days from the time the products are made available at
the place of delivery stated in the order confirmation. If the customer refuses or delay delivery without Metra's agreement,
the customer must pay Metra's expenses or loss resulting from that refusal, including storage costs, until you accept delivery.
Nothing in this agreement affects Metra's right to cancel or reject any order at any time
'''
            sheet.merge_range(table_row, 0, table_row, 8,'1. Quotations/Orders/Contract', format_6)
            table_row += 1

            sheet.merge_range(table_row, 0, table_row, 8,text_term_one, format_5)
            table_row += 2

            sheet.merge_range(table_row, 0, table_row, 8,'2. Pricing', format_6)
            table_row += 1
            text_term_2='''Products and service offering prices, tax, shipment, insurance and installation are as shown on the invoice. Changes to
exchange rates, duties, insurance, freight, market condition, and purchase costs (incl. for components and Services) may
cause Metra to adjust prices accordingly.
'''
            sheet.merge_range(table_row, 0, table_row, 8,text_term_2, format_5)
            table_row += 2
            sheet.merge_range(table_row, 0, table_row, 8,'3. Payment Terms & Payment Obligation', format_6)
            table_row += 1
            text_term_3='''
Payment will be made as agreed in writing by Metra or in absence of such agreement, within 30 days of the invoice date
without further notice from Metra. Payment timing is of the essence. Metra may suspend deliveries or Service until full
payment for that order. If payment is late, Metra may charge a late payment charge of 2% monthly accruing on a day-to-day
basis for each day of late payment, subject to maximum limitation by law, (unless we otherwise elect) on the overdue amount,
and the costs of recovery shall be payable by the customer. The customer agrees that all invoices and any other amounts due
under this agreement are payable solely to us in the currency of payment stated above, in full without any set off, counter-
claims, abatement, or reduction. We may at our sole discretion apply payments made to us (whether by you or otherwise) to
pay late payment charges, invoices overdue interest, or any outstanding amounts. The customer must pay all sums due to us
under this agreement including invoices and other charges to us in full, without abatement, discount, reduction, set off,
dispute or counterclaim. The customer will not assert against Metra any claims the customer may have against any third party
including the manufacturer or original supplier or shipper of goods. We have no obligation to perform any obligation by any
third party. Metra may set off against any amounts owed by Metra to the customer any amount dues from the customer to
Metra (including those prospectively or contingently due where in our reasonable opinion they are likely to become payable)
'''
            sheet.merge_range(table_row, 0, table_row, 8,text_term_3, format_5)
            table_row += 2
            sheet.merge_range(table_row, 0, table_row, 8,'4. Delivery/Title/Risk', format_6)
            table_row += 1
            text_term_4='''
The Delivery period in the Order Confirmation is approximate. Partial deliveries may be made. The place of delivery is stated
in the Order Confirmation. Title to Product passes on full payment and until then the customer must insure the goods and the
customer must not modify or pledge them. The customer may use the goods, without modification, in the ordinary course of
business. Metra reserves the rights to enter the storage premises to repossess the goods. If the customer sells them before
title passes, the customer will become Metra's agent and the proceeds of such sale shall be held on Metra's behalf separately
from the customer's general funds. Metra may sue for the Price before title passes. If the customer refuses delivery without
Metra's agreement, the customer must pay Metra's expenses or loss resulting from that refusal, including storage costs, until
the customer accepts delivery. All risk of the loss of the goods passes to the customer upon delivery. Any missing or damaged
packaging should be noted on the waybill prior to signing it by the customer or its nominated shipping agent.
'''
            sheet.merge_range(table_row, 0, table_row, 8,text_term_4, format_5)
            table_row += 2
            sheet.merge_range(table_row, 0, table_row, 8,'5. Trade and Import Authorizations', format_6)
            table_row += 1
            text_term_5='''
The customer hereby warrant and represent that the customer have and shall continue to have the due authorizations and
licenses necessary and required to purchase the Products and any other products purchased from the Supplier and to import
the same into the relevant country. Any failure by the customer to clear the Products from the relevant customs or other
authorities in the relevant county whether due to the failure to obtain or maintain the requisite authorizations or licenses or
for any other reason whatsoever, will not invalidate this agreement and the customer shall remain bound by the terms of this
agreement including liability to make payments to Metra under the terms of this Agreement
'''
            sheet.merge_range(table_row, 0, table_row, 8,text_term_5, format_5)
            table_row += 2
            sheet.merge_range(table_row, 0, table_row, 8,'6. Acceptance', format_6)
            table_row += 1
            tetx_term_6='''
When the customer or its nominated shipping agent receive the products, the customer or its nominated shipping agent must
inspect the products for any defects or non-conformity, and if any, the customer must notify Metra immediately and mention
any discrepancies on the proof of delivery. After this, the customer will have accepted Product. If Metra agrees to the return
of Product at its choosing, it must be in its original condition with packaging, a return note and proof of purchase;
'''
            sheet.merge_range(table_row, 0, table_row, 8,tetx_term_6, format_5)
            table_row += 2
            sheet.merge_range(table_row, 0, table_row, 8,'7. Export Control', format_6)
            table_row += 1
            text_term_7='''The customer acknowledge that Product may include technology and Software which is subject to US and EU export control
laws and laws of the country where it is delivered or used: the customer must abide by all these laws. Product may not be sold,
leased or transferred to restricted / embargoed end users or countries or for a user involved in weapons of mass destruction
or genocide without the prior consent of the US or competent EU government. The customer understands and acknowledges
that US and EU restrictions vary regularly and depending on Product, therefore you must refer to the current US and EU
regulations.
'''
            sheet.merge_range(table_row, 0, table_row, 8,text_term_7, format_5)
            table_row += 2
            sheet.merge_range(table_row, 0, table_row, 8,'8. Foreign Corrupt Practices Act ("FCPA")', format_6)
            table_row += 1
            tetx_term_8='''
Each Party shall comply with all applicable laws and regulations enacted to combat bribery and corruption, including the
United States Foreign Corrupt Practices Act ("FCPA"), the local Bribery Acts, the principles of the OECD Convention on
Combating Bribery of Foreign Public Officials (the "OECD Convention") and any corresponding laws of all countries where
business or services will be conducted or performed pursuant to this Agreement. Any amounts paid by Supplier to Introducer
pursuant to the terms of this Agreement will be for the services actually rendered, or products sold, in accordance with the
terms of this Agreement. Introducer shall not directly or indirectly through a third party pay, offer, promise to pay, or give
anything of value (including any amounts paid or credited by Supplier to Introducer) to any person including an employee or
official of a government, government controlled enterprise or company, or vendor or customer or political party, with the
reasonable knowledge that it will be used for the purpose of obtaining any improper benefit or to improperly influence any act
or decision Supplier to Introducer to any person including an employee or official of a government, government controlled
enterprise or company, or vendor or customer or political party, with the reasonable knowledge that it will be used for the
purpose of obtaining any improper benefit or to improperly influence any act or decision by such person or party for the
purpose of obtaining, retaining, or directing business.
'''
            sheet.merge_range(table_row, 0, table_row, 8,tetx_term_8, format_5)
            table_row += 2
            sheet.merge_range(table_row, 0, table_row, 8,'9. Confidentiality', format_6)
            table_row += 1
            tetx_term_8='''Each party must treat all information received from the other marked "confidential" or reasonably obvious to be confidential
as it would treat its own confidential information.
'''
            sheet.merge_range(table_row, 0, table_row, 8,tetx_term_8, format_5)
            

       