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
            col_num = 0
            sheet.write(13,col_num,'Items',format_2) 
            col_num+=1   
            sheet.write(13,col_num,'Part Number',format_2)    
            col_num+=1
            sheet.merge_range(13, col_num ,13,col_num + 2 ,'Product Description',format_2)
            col_num+=3
            if obj._check_duration_visiblity():
                print('-----------------------------')
                sheet.write(13,col_num,'Duration (Months)',format_2)
                col_num+=1    


  
            sheet.write(13,col_num,'Quantity',format_2)   
            col_num+=1 
            sheet.write(13,col_num,'Unite Price',format_2)    
            col_num+=1
            sheet.write(13,col_num,'Total price',format_2) 
            col_num+=1

            section_format = workbook.add_format({'bold':True,'font_size': 11,'text_wrap': True})



            index = 1
            for product in obj.order_line:
                # vat_percentage = str(int(product.tax_id.amount)) + "%"
                val_col_num = 0
                if product.display_type == 'line_section':
                    sheet.merge_range(table_row, 0, table_row, 8, product.name or "",section_format)
                elif product.display_type == 'line_note':
                    sheet.merge_range(table_row, 0, table_row, 8, product.name or "",section_format)
                else:
                    sheet.write(table_row, val_col_num, product.line_number or index, center)
                    val_col_num+=1
                    sheet.write(table_row, val_col_num, product.product_template_id.name or "")
                    val_col_num+=1
                    sheet.merge_range(table_row, val_col_num, table_row, val_col_num + 2, product.name or "")
                    val_col_num+=3
                    if obj._check_duration_visiblity():
                        sheet.write(table_row, val_col_num, product.duration or "N/A", center)
                        val_col_num+=1


                    sheet.write(table_row, val_col_num, product.product_uom_qty or "", center)
                    val_col_num+=1
                    sheet.write(table_row, val_col_num, product.price_unit or "", currency)
                    val_col_num+=1
                    sheet.write(table_row, val_col_num, product.price_subtotal or "", currency)
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




            sheet.conditional_format(f"A{table_row}:I{table_row+100}",{'type':'formula','criteria': True,'format':white_bg})

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
            sheet.merge_range(table_row, 0, table_row, 8,'1. ACCEPTANCE OF TERMS', format_6)
            table_row += 1

            text_term_one_1='''1.1. By accepting delivery of the products whether full or partial delivery, You agree and accept to be bound by these terms and conditions (“Terms”)
'''
          
            text_term_one_2='''1.2. These Terms govern the sale, purchase and use of products of any nature whether physical or otherwise, or Services.
            '''
            text_term_one_3='''1.3. If you have accepted these Terms on behalf of another party, you represent and warrant that you have the full authority to bind such party to these Terms.
            '''
            text_term_one_4='''1.4. All sales shall be made by the Seller exclusively on the basis of these General Terms and Any additional, preprinted or different terms contained on any purchase order, portal, or other communication from Buyer purporting to apply shall be deemed void and unenforceable unless otherwise accepted by the Seller.
            '''
            

            sheet.merge_range(table_row, 0, table_row, 8,text_term_one_1, format_5)
            table_row += 1

            sheet.merge_range(table_row, 0, table_row, 8,text_term_one_2, format_5)
            table_row += 1

            sheet.merge_range(table_row, 0, table_row, 8,text_term_one_3, format_5)
            table_row += 1

            sheet.merge_range(table_row, 0, table_row, 8,text_term_one_4, format_5)
            table_row += 2

            sheet.merge_range(table_row, 0, table_row, 8,'2. Returns', format_6)
            table_row += 1
            text_term_2='''To the greatest extent permitted under applicable law, any warranty from the Seller in relation to defects in the Products sold by the Seller (including warranty for defects in materials, workmanship, merchantability, or fitness for a particular use, or any other warranty) is hereby expressly excluded, unless otherwise accepted by the Seller in writing. To the extent that the manufacturer of the Products provide separate warranties for the benefit of the Buyer or the Buyer's customers, then such persons may enforce such Supplier and/or manufacturer warranties in accordance with the terms and conditions applicable to them, at no cost or liability for the Seller.
'''
            sheet.merge_range(table_row, 0, table_row, 8,text_term_2, format_5)
            table_row += 2
            sheet.merge_range(table_row, 0, table_row, 8,'3. Pricing', format_6)
            table_row += 1
            text_term_3='''Products and/or service offering prices, tax, shipment, insurance and installation are as shown on the invoice. Changes to exchange rates, duties, insurance, freight, market condition, and purchase costs (including for components and services) may cause Metra to adjust prices accordingly.

'''
            sheet.merge_range(table_row, 0, table_row, 8,text_term_3, format_5)
            table_row += 2
            sheet.merge_range(table_row, 0, table_row, 8,'4. Payment', format_6)
            table_row += 1
            text_term_4_1='''4.1. Buyer shall pay the price indicated on the invoice according to the payment terms identified therein. In the case of absence of any specific payment terms, the price will be due immediately.
'''
            text_term_4_2='''4.2. In case the Buyer disputes the invoice, the Buyer must provide notice of such dispute within five (5) days from the date of the invoice or else it is deemed to have accepted the invoice undisputedly.
            '''
            text_term_4_3='''4.3. In case the Buyer fails to pay the total sums due on an invoice by the due date or in case of the Buyer’s insolvency or bankruptcy, the entire outstanding balance due to Seller on any other invoices owed by the Buyer shall be accelerated and become due in full immediately.

            '''
            text_term_4_4='''4.4. Metra may suspend deliveries or Service, whether such delivery or service is subject to this invoice or not, until full payment for that order. If payment is late, the Buyer shall be liable to liquidated damages equivalent to 2% monthly accruing on a day-to-day basis for each day of late payment and the costs of recovery shall be payable by the customer. This shall be additional to any late payment interest enforced by any applicable law.
            '''
            text_term_4_5='''4.5. Seller shall be entitled, in addition to all other remedies available at law or under these Terms, to recover reasonable attorneys’ fees, legal costs and/or any other expenses incurred in collecting all outstanding sums from Buyer or otherwise enforcing or successfully defending these Terms.
            '''
            sheet.merge_range(table_row, 0, table_row, 8,text_term_4_1, format_5)
            table_row += 1

            sheet.merge_range(table_row, 0, table_row, 8,text_term_4_2, format_5)
            table_row += 1

            sheet.merge_range(table_row, 0, table_row, 8,text_term_4_3, format_5)
            table_row += 1

            sheet.merge_range(table_row, 0, table_row, 8,text_term_4_4, format_5)
            table_row += 1

            sheet.merge_range(table_row, 0, table_row, 8,text_term_4_5, format_5)
            table_row += 2

            sheet.merge_range(table_row, 0, table_row, 8,'5. Set-off', format_6)
            table_row += 1
            text_term_5_1=''' 5.1. The Buyer must pay all sums due to the Seller under any order, including invoices and other charges in full, without abatement, discount, reduction, set off, dispute or counterclaim. 

'''
            text_term_5_2='''5.2. The Buyer shall not be entitled to against the Seller any claims it may have against any third party including the manufacturer or Supplier or shipper of Products. 

            '''
            text_term_5_3='''5.3. The Seller may set off against any amounts owed to the Buyer any amounts due from the Buyer to the Seller (including those prospectively or contingently due which are, in the Seller’s reasonable discretion, likely to become payable).

            '''
            sheet.merge_range(table_row, 0, table_row, 8,text_term_5_1, format_5)
            table_row += 1
            sheet.merge_range(table_row, 0, table_row, 8,text_term_5_2, format_5)
            table_row += 1
            sheet.merge_range(table_row, 0, table_row, 8,text_term_5_3, format_5)
            table_row += 2
            sheet.merge_range(table_row, 0, table_row, 8,'6. Delivery', format_6)
            table_row += 1
            tetx_term_6_1='''6.1. Delivery terms are set for indicative purposes only and shall not be binding on the Seller.  To the greatest extent permitted under applicable law, any warranty from the Seller or liability in relation to the timely delivery of the Products in accordance with the Contract is hereby excluded.
'''
            tetx_term_6_2='''6.2. In the event Buyer, verbally or in writing, confirms a delivery date with Seller but subsequently suspends the Order or is unable to accept delivery, Buyer shall reimburse Seller for all costs and expenses Seller incurs as a result thereof, including, but not limited to, reasonable storage costs.
            '''
            tetx_term_6_3='''6.3. The Products shall remain the property of Seller until their price has been paid in full to the benefit of the Seller or any assignee thereof. The Buyer shall diligently hold the unsold Products in custody on behalf of the Seller and shall ensure that the Products will not be damaged, modified, or subject to deterioration while title is retained by the Seller. In case of the Buyer’s failure to pay the Products’ price, the Seller may reclaim the goods on account of the retention of title. If the customer sells them before title passes, the customer will become Metra's agent and the proceeds of such sale shall be held on Metra's behalf separately from the customer's general funds.
            '''
            tetx_term_6_4='''6.4. If the customer refuses delivery without Metra's agreement, the customer must pay Metra's expenses or loss resulting from that refusal, including without limitation storage costs, demurrages, etc. until the customer accepts delivery of the entire order.
            '''
            tetx_term_6_5='''6.5. The risk of the loss of the goods shall pass to the customer upon delivery. Any missing or damaged packaging should be noted on the proof of delivery prior to signing it by the customer or its nominated shipping agent. Absence of such notice shall be proof of delivery of the products without any discrepancy. 
            '''
         
            sheet.merge_range(table_row, 0, table_row, 8,tetx_term_6_1, format_5)
            table_row += 1
            sheet.merge_range(table_row, 0, table_row, 8,tetx_term_6_2, format_5)
            table_row += 1
            sheet.merge_range(table_row, 0, table_row, 8,tetx_term_6_3, format_5)
            table_row += 1
            sheet.merge_range(table_row, 0, table_row, 8,tetx_term_6_4, format_5)
            table_row += 1
            sheet.merge_range(table_row, 0, table_row, 8,tetx_term_6_5, format_5)
            table_row += 2

            sheet.merge_range(table_row, 0, table_row, 8,'7. Compliance with laws and requirements', format_6)
            table_row += 1
            text_term_7_1='''7.1. Each party shall comply with all applicable laws, rules and regulations, including but not limited to, export and import, trade restrictions, FARs, anti-bribery and anti-corruption, anti-money laundering, anti-human trafficking and slavery, environmental protection, and health and safety.
'''
            text_term_7_2='''7.2. The Buyer undertakes to hold the Seller harmless from any costs, losses, or damages the Seller may suffer as a result of any non-compliance of applicable laws on the part of the Buyer, including as a result of third-party claims.
            '''
            text_term_7_3='''7.3. Products and Software may be subject to export controls under the laws, regulations, sanctions and/or directives of the United States and other countries where its delivered or used.
            '''
            text_term_7_4='''7.4. The customer hereby warrants and represent that the customer have and shall continue to have the due authorizations and licenses necessary and required to purchase the Products and any other
            products purchased from the Supplier and to import the same into the relevant country. Any failure by the customer to clear the Products from the relevant customs or other authorities in the relevant county whether due to the failure to obtain or maintain the requisite authorizations or licenses or for any other reason whatsoever, will not invalidate this agreement and the customer shall remain bound by the terms of this agreement including liability to make payments to Metra under the terms of this Agreement.
            '''
            text_term_7_5='''7.5. The customer acknowledge that Product may include technology and Software which is subject to US and EU export control laws and laws of the country where it is delivered or used: the customer must abide by all these laws. Product may not be sold, leased or transferred to restricted / embargoed end users or countries or for a user involved in weapons of mass destruction or genocide without the prior consent of the US or competent EU government. The customer understands and acknowledges that US and EU restrictions vary regularly and depending on Product, therefore you must refer to the current US and EU regulations.
            '''
            sheet.merge_range(table_row, 0, table_row, 8,text_term_7_1, format_5)
            table_row += 1
            sheet.merge_range(table_row, 0, table_row, 8,text_term_7_2, format_5)
            table_row += 1
            sheet.merge_range(table_row, 0, table_row, 8,text_term_7_3, format_5)
            table_row += 1
            sheet.merge_range(table_row, 0, table_row, 8,text_term_7_4, format_5)
            table_row += 1
            sheet.merge_range(table_row, 0, table_row, 8,text_term_7_5, format_5)
            table_row += 2

            sheet.merge_range(table_row, 0, table_row, 8,'8. Product Liability', format_6)
            table_row += 1
            tetx_term_8='''To the greatest extent permitted under applicable law, any liability of the Seller for damages caused by the Products (including damages to third parties and injuries) is hereby expressly excluded to the extent that such damages are not a direct and immediate consequence of the Seller's gross negligence or wilful misconduct.
'''
            sheet.merge_range(table_row, 0, table_row, 8,tetx_term_8, format_5)
            table_row += 2
            sheet.merge_range(table_row, 0, table_row, 8,'9. Limitation of liability', format_6)
            table_row += 1
            tetx_term_9='''Regardless of the previous paragraphs, if the Seller is found to be liable for any reason whatsoever, to the greatest extent permitted under applicable law the Seller's liability to the Buyer or to any third party is limited to the value of the order from which the liability arose. Should the maximum liability amount under the applicable law be less the value of the order from which the liability arose, then the Seller’s liability shall be limited to such amount.
'''
            sheet.merge_range(table_row, 0, table_row, 8,tetx_term_9, format_5)
            table_row += 2

            sheet.merge_range(table_row, 0, table_row, 8,'10. Indemnity', format_6)
            table_row += 1
            tetx_term_10='''Buyer shall indemnify and defend Seller and its affiliates, directors, officers, affiliates, employees, agents, successors, and permitted assigns (“Indemnitees”) against any claims, demands, damages, liabilities and expenses (including court costs and reasonable attorneys ‘fees) that Indemnitees incur as a result of or in connection with: (a) any third-party claims arising from Buyer’s use of the Products or Services in any manner(e.g., solely or in combination) not expressly permitted by these Terms or the applicable license agreement or specifications provided by the Product and/or Software manufacturer or provider of Services; (b) Indemnitees’ compliance with any technology, designs, instructions or requirements, including any specifications provided by Buyer or a third party on Buyer’s behalf ; and (c) any reasonable costs and attorneys’ fees and expenses required for Indemnitees to respond to a subpoena, court order or other official government inquiry regarding Buyer’s use of the Products, Software, or Services.
'''
            sheet.merge_range(table_row, 0, table_row, 8,tetx_term_10, format_5)
            table_row += 2

            sheet.merge_range(table_row, 0, table_row, 8,'11. Acknowledgments and Undertakings by the Buyer', format_6)
            table_row += 1
            tetx_term_11_1='''11.1. The Buyer undertakes to notify the Seller in writing upon the occurrence of any event which leads or could lead to its insolvency;
'''
            tetx_term_11_2='''11.2. the Buyer undertakes to use reasonable measures to prevent, mitigate and minimise any loss which the Seller may incur, and to cooperate with the Seller in taking all reasonable steps to prevent, mitigate and/or minimise such loss;
            '''
            tetx_term_11_3='''11.3. the Buyer undertakes to inform the Seller immediately in case of any changes in its shareholding structure, its management or any other form of change which could result in the Buyer’s inability to fulfil its contractual obligations or which would decrease the value of any securities or guarantees granted by the Buyer to the Seller, if any. In case of such change, the Seller shall have the right to reassess the Buyer’s creditworthiness and determine, at its sole discretion, if it wishes to terminate the relationship;
            '''
            tetx_term_11_4='''11.4. Buyer acknowledges and agrees that, in performing its obligations under these Terms, Seller will rely upon the accuracy and completeness of the information and documentation Buyer provides, and that Seller’s performance is dependent on Buyer’s provision of complete and accurate information and data. It is Buyer’s responsibility to ensure that the Products and Services are the ones that it has requested and that all specifications and quantities are correct., and undertakes to indemnify the Seller for any losses, damages or costs whatsoever which could result from the Buyer’s breach of this obligation;
            '''
            tetx_term_11_5='''11.5. The Buyer agrees that all invoices and any other amounts due under this agreement are payable in full without any set off, counterclaims, abatement, or reduction and in the currency of payment stated in the invoice to be issued by the Seller. The Buyer further accepts that the Seller may, at its sole discretion, apply payments made, whether by Buyer or otherwise, to pay late payment charges, invoices overdue interest, or any outstanding amounts.
            '''
            tetx_term_11_6='''11.6. The Buyer acknowledges, understands and agrees that by signing the Proof of Delivery document without any discrepancies, the Products are considered irrevocably accepted, whether such delivery was conducted by the Supplier directly or by the Seller. The Buyer further acknowledges and understands that by signing the Proof of Delivery document without discrepancy, it shall have no right, under any case whatsoever, to initiate any claims against the Seller for any defect or non-conformity of any kind in relation to the received Products.
            '''
            sheet.merge_range(table_row, 0, table_row, 8,tetx_term_11_1, format_5)
            table_row += 1
            sheet.merge_range(table_row, 0, table_row, 8,tetx_term_11_2, format_5)
            table_row += 1
            sheet.merge_range(table_row, 0, table_row, 8,tetx_term_11_3, format_5)
            table_row += 1
            sheet.merge_range(table_row, 0, table_row, 8,tetx_term_11_4, format_5)
            table_row += 1
            sheet.merge_range(table_row, 0, table_row, 8,tetx_term_11_5, format_5)
            table_row += 1
            sheet.merge_range(table_row, 0, table_row, 8,tetx_term_11_6, format_5)
            table_row += 2

            sheet.merge_range(table_row, 0, table_row, 8,'12. Force majeure', format_6)
            table_row += 1
            tetx_term_12='''Seller shall not be liable for any failure to perform its obligations under an Order or Scope of Work (“SOW”) resulting directly or indirectly from, or contributed to or by acts of God, acts of terrorism, civil or military authority, epidemic or pandemic, fires, strikes or other labor disputes, accidents, floods, war, riot, inability to secure raw material or transportation facilities, hacking or other malicious attack, dissolution of the applicable manufacturer’s business, acts or omissions of carriers, or any other circumstances beyond Seller’s reasonable control.
'''
            sheet.merge_range(table_row, 0, table_row, 8,tetx_term_12, format_5)
            table_row += 2

            sheet.merge_range(table_row, 0, table_row, 8,'13. Confidentiality', format_6)
            table_row += 1
            tetx_term_13_1='''13.1. Neither Party may disclose any information (i) that is marked or labelled “Confidential”, “Secret” or the like at the moment of disclosure or, in case of oral Information, is identified as confidential, (ii) of which the confidential nature is reasonably apparent. For the avoidance of doubt, any information relating in any way, directly or indirectly, to the price of the Products or the payment terms thereof shall be considered confidential (“Confidential Information”);
'''
            tetx_term_13_2='''13.2. The confidentiality obligations under these Terms shall not apply to Confidential Information of which the receiving Party can demonstrate by means of dated documentation that such Confidential Information: (i) was already in the public domain at the time it was disclosed or subsequently enters the public domain through no fault of the receiving Party, (ii) was developed by the receiving Party independently and without use of Confidential Information provided by the disclosing Party under these Terms and without any breach thereof, or (iii) is required to be disclosed pursuant to the requirement, order or directive of a government agency or by operation of law subject to prior consultation with disclosing Party's legal counsel.
            '''
            sheet.merge_range(table_row, 0, table_row, 8,tetx_term_13_1, format_5)
            table_row += 1
            sheet.merge_range(table_row, 0, table_row, 8,tetx_term_13_2, format_5)
            table_row += 2

            sheet.merge_range(table_row, 0, table_row, 8,'14. Anti-Bribery and Corruption', format_6)
            table_row += 1
            tetx_term_14_1='''14.1.  The buyer undertakes that it has not and will not, and none of its employees, officers, directors, contractors, subcontractors and agents has or will, directly or indirectly, pay, give, deliver, receive or agree (or undertake to pay, give, deliver, receive or agree) any bribe, pay-off, kickback, gift, gratuity, commission, amount or other thing of value, or any interest-free loans, contributions or donations, in any way or form and whether in local or foreign currency, in the country where the Services are provided or any other place where such conduct relates to the Agreement, , to any third party, including any non-U.S. official, in each case, in violation of the Foreign Corrupt Practices Act of 1977 (the FCPA), the U.K. Bribery Act 2010, or any other applicable antibribery or anti-corruption law.
'''
            tetx_term_14_2='''14.2. The Buyer further represents that it shall, and shall cause each of its subsidiaries or affiliates to, cease all of its or their respective activities, as well as remediate any actions taken by the Buyer, its subsidiaries or affiliates, or any of their respective directors, officers, managers, employees, independent contractors, representatives or agents in violation of the FCPA, the U.K. Bribery Act 2010, or any other applicable anti-bribery or anticorruption law.
            '''
            sheet.merge_range(table_row, 0, table_row, 8,tetx_term_14_1, format_5)
            table_row += 1
            sheet.merge_range(table_row, 0, table_row, 8,tetx_term_14_2, format_5)
            table_row += 2

            sheet.merge_range(table_row, 0, table_row, 8,'15. Governing Law and Arbitration', format_6)
            table_row += 1
            tetx_term_15_1='''15.1. These Terms shall in all respects be governed by the laws of the United Arab Emirates. The terms of the UN Convention on Contracts for the International Sale of Goods of 1980 (and any amendments or successors thereto) are hereby excluded.
'''
            tetx_term_15_2='''15.2. Any dispute between the Parties under or in connection with this Invoice as well as its corresponding purchase order(s) (including,  any question regarding its existence, validity or termination) which cannot be resolved amicably arbitration in accordance with the rules of arbitration of the Cairo Regional Centre for International Commercial Arbitration (CRCICA). The number of arbitrators shall be one. The language of arbitration shall be English. The seat of arbitration shall be Paris, France, however, the venue for the arbitral proceedings shall be Cairo, Egypt, Despite that, in case Metra is the claimant, Metra may, at its sole discretion, submit any such dispute to the local courts in the jurisdiction where the Buyer is domiciled. The Buyer hereby irrevocably waives any objection to the jurisdiction, process and venue of any such court and to the effectiveness, execution and enforcement of any order or judgment (including, but not limited to, a default judgment) of any such court in relation to these Terms, to the maximum extent permitted by the law.
            '''
            sheet.merge_range(table_row, 0, table_row, 8,tetx_term_15_1, format_5)
            table_row += 1
            sheet.merge_range(table_row, 0, table_row, 8,tetx_term_15_2, format_5)
            table_row += 2
            




    

      



