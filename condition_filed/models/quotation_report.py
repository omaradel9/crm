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
        sheet.set_column(9, 9, 20)


       
      
        sheet.merge_range(6, 0 , 6 ,9,'Quotation',format_1)
        sheet.conditional_format(f'A1:J6',{'type':'formula','criteria': True,'format':white_bg}) 

        sheet.conditional_format(f'A7:J7',{'type':'formula','criteria': True,'format':qt_border}) 
         
        sheet.conditional_format(f'A8:J12',{'type':'formula','criteria': True,'format':white_bg})
        
        sheet.conditional_format(f'A12:J12',{'type':'formula','criteria': True,'format':border_top})

        sheet.conditional_format(f'A12:J13',{'type':'formula','criteria': True,'format':white_bg}) 
 

 
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
            if obj.po_no: 
                sheet.merge_range(row, 5 ,row,6,'PO.No:',bold)
                sheet.write(row, 7,obj.po_no or "")
                row += 1 
            
            bold_static = workbook.add_format({'bold':True,'font_size': 9,'text_wrap': True})
            sheet.merge_range(row, 0 ,row,8,'We will be happy to supply any further information you may need and trust that your call on us to fill your order, which will receive our prompt and careful attention.',bold_static)
            row += 1
            sheet.merge_range(row, 0 ,row,8,'We are pleased to quote you the following:',bold_static)
            col_num = 0
            sheet.write(13,col_num,'Items',format_2) 
            col_num+=1   
            sheet.write(13,col_num,'Metra Code',format_2)    
            col_num+=1
            sheet.write(13,col_num,'MPN',format_2)    
            col_num+=1
            sheet.merge_range(13, col_num ,13,col_num + 2 ,'Product Description',format_2)
            col_num+=3
            if obj._check_duration_visiblity():
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
                    sheet.merge_range(table_row, 0, table_row, 9, product.name or "",section_format)
                elif product.display_type == 'line_note':
                    sheet.merge_range(table_row, 0, table_row, 9, product.name or "",section_format)
                else:
                    sheet.write(table_row, val_col_num, product.line_number or index, center)
                    val_col_num+=1
                    sheet.write(table_row, val_col_num, product.product_template_id.name or "")
                    val_col_num+=1
                    sheet.write(table_row, val_col_num, product.alt_barcode or "")
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


            if obj._check_duration_visiblity():
                sheet.merge_range(table_row,0,table_row,8,'Sub Totals In USD Excluding VAT',format_3)
                sheet.write(table_row, 9,obj.amount_untaxed or "", currency)

                table_row += 1
                if obj.term_conditions_id.tax:
                        vat_str = f'Value-Added Tax (VAT) ({obj.term_conditions_id.tax})'
                else:
                        vat_str = f'Value-Added Tax (VAT) (0)'
            
                sheet.merge_range(table_row,0,table_row,8,vat_str,format_3) 
                sheet.write(table_row, 9,obj.amount_tax or "", currency)
            
                table_row += 1
                
                
                sheet.merge_range(table_row,0,table_row,8,'Total Prices In USD Including VAT',format_3)  
                sheet.write(table_row, 9,obj.amount_total or "", currency) 

                table_row += 1
            else:
                sheet.merge_range(table_row,0,table_row,8,'Sub Totals In USD Excluding VAT',format_3)
                sheet.write(table_row, 9,obj.amount_untaxed or "", currency)

                table_row += 1
                if obj.term_conditions_id.tax:
                        vat_str = f'Value-Added Tax (VAT) ({obj.term_conditions_id.tax})'
                else:
                        vat_str = f'Value-Added Tax (VAT) (0)'
            
                sheet.merge_range(table_row,0,table_row,8,vat_str,format_3) 
                sheet.write(table_row, 9,obj.amount_tax or "", currency)
            
                table_row += 1
                
                
                sheet.merge_range(table_row,0,table_row,8,'Total Prices In USD Including VAT',format_3)  
                sheet.write(table_row, 9,obj.amount_total or "", currency) 

                table_row += 1    
    

                

               

            
            sheet.conditional_format(f"A14:I{table_row}",{'type':'formula','criteria': True,'format':table_border})
            sheet.conditional_format(f"J14:J{table_row}",{'type':'formula','criteria': True,'format':left_border})




            sheet.conditional_format(f"A{table_row}:J{table_row+100}",{'type':'formula','criteria': True,'format':white_bg})

            table_row +=1
            if obj.pricelist_id.currency_id:
                sheet.set_row(table_row,30)
                sheet.merge_range(table_row, 0, table_row, 2, 'Currency:', format_4)
                sheet.merge_range(table_row, 3, table_row, 9, obj.pricelist_id.currency_id.name, format_4)
                table_row += 2
            if obj.brand_id:
                sheet.set_row(table_row,30)
                sheet.merge_range(table_row, 0, table_row, 2, 'Usage:', format_4)
                sheet.merge_range(table_row, 3, table_row, 9, obj.brand_id.name, format_4)
                table_row += 2    
            # if obj.pricelist_id.currency_id:
            #     sheet.set_row(table_row,30)
            #     sheet.merge_range(table_row, 0, table_row, 2, 'Currency:', format_4)
            #     sheet.merge_range(table_row, 3, table_row, 8, obj.pricelist_id.currency_id.name, format_4)
            #     table_row += 2   
            if  obj.amount_total:
                sheet.set_row(table_row,30) 
                sheet.merge_range(table_row, 0, table_row, 2, 'Total in Word:', format_4)
                sheet.merge_range(table_row, 3, table_row, 9, num2words(obj.amount_total).upper(), format_4)

                table_row += 2
            if obj.payment_term_id:
                sheet.set_row(table_row,30)
                soup = BeautifulSoup(obj.payment_term_id.note, 'html.parser')
                payment = soup.get_text()  
                sheet.merge_range(table_row, 0, table_row, 2, 'Payment Terms:', format_4)
                sheet.merge_range(table_row, 3, table_row, 9, payment, format_4)
                table_row += 2
            if obj.payment_method:
                sheet.set_row(table_row,30) 
                sheet.merge_range(table_row, 0, table_row, 2, 'Payment Method:', format_4)
                sheet.merge_range(table_row, 3, table_row, 9, obj.payment_method, format_4)
                table_row += 2
            if obj.incoterms:
           
                sheet.set_row(table_row,30)  
                soup = BeautifulSoup(obj.incoterms, 'html.parser')
                print('-----------------------------==============',soup)
                incoterms = soup.get_text()  
                # incoterms = soup.get_text().replace('<br>', '\n')
                sheet.merge_range(table_row, 0, table_row, 2, 'Incoterms:', format_4)
                sheet.merge_range(table_row, 3, table_row, 9, incoterms, format_4)
                table_row += 2
            if obj.delivery_location:
                sheet.set_row(table_row,30)   
                sheet.merge_range(table_row, 0, table_row, 2, 'Delivery Location:', format_4)
                sheet.merge_range(table_row, 3, table_row, 9, obj.delivery_location, format_4)
                table_row += 2
            if obj.mode_of_shipment:
                sheet.set_row(table_row,30)
                sheet.merge_range(table_row, 0, table_row, 2, 'Mode of Shipment:', format_4)
                sheet.merge_range(table_row, 3, table_row, 9, obj.mode_of_shipment, format_4)
                sheet.set_row(table_row, None, None, {'level': 1, 'hidden': False, 'collapsed': False, 'autofit': True})

                table_row += 2
            if obj.end_user_id:
                sheet.set_row(table_row,30)   
                sheet.merge_range(table_row, 0, table_row, 2, 'End Customer:', format_4)
                sheet.merge_range(table_row, 3, table_row, 9, obj.end_user_id.name, format_4)
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
            sheet.merge_range(table_row, 0, table_row, 9,text_one, format_5)
            table_row += 2 


            sheet.merge_range(table_row, 0, table_row, 9,text_two, format_5)
            table_row += 2

            sheet.merge_range(table_row, 0, table_row, 9,text_three, format_5)
            table_row += 2



            sheet.merge_range(table_row, 0, table_row, 9,'Terms and Conditions', format_6)
            table_row += 1

            sheet.merge_range(table_row, 0, table_row, 9,'Metra Computer Group', format_6)
            table_row += 3
            sheet.merge_range(table_row, 0, table_row, 9,'1. Definitions', format_6)
            table_row += 1

            text_term_one_1='''In any Metra communication, including any quotation, order, invoice, the following expressions shall, unless the context otherwise admits, carry the meaning respectively assigned to them hereunder:
'''
            sheet.merge_range(table_row, 0, table_row, 9,text_term_one_1, format_5)
            table_row += 2




            sheet.merge_range(table_row, 0, table_row, 2,'1.1 “Sold-to party” or “Customer”', format_5)
            sheet.merge_range(table_row, 3, table_row, 9,'An entity that places an order for goods or services. The Sold-to party or Customer can be, but is not necessarily, the Bill-to party, Ship-to party, or the Payer.', format_5)
            table_row += 2
            sheet.merge_range(table_row, 0, table_row, 2,'1.2 “Product(s)”', format_5)
            sheet.merge_range(table_row, 3, table_row, 9,'The goods sold and/or services provided from Metra to the Customer in a given transaction, including but not limited to hardware products, software licenses, warranty, and services.', format_5)
            table_row += 2
            sheet.merge_range(table_row, 0, table_row, 2,'1.3 “Payer”', format_5)
            sheet.merge_range(table_row, 3, table_row, 9,'An entity that has the obligation to pay a bill or invoice to Metra, including VAT if applicable, as nominated by the Customer.', format_5)
            table_row += 2
            sheet.merge_range(table_row, 0, table_row, 2,'1.4 “Bill-to party”', format_5)
            sheet.merge_range(table_row, 3, table_row, 9,'An entity nominated by the Customer to whom Metra shall send its invoices for payment of the Products price or any other dues under these terms and conditions.', format_5)
            table_row += 2
            sheet.merge_range(table_row, 0, table_row, 2,'1.5 “Ship-to party”', format_5)
            sheet.merge_range(table_row, 3, table_row, 9,'Any entity that will receive the Products from Metra. This can be either the Customer or a third party nominated by the Customer. ', format_5)
            table_row += 2
            sheet.merge_range(table_row, 0, table_row, 2,'1.6 “End-User”', format_5)
            sheet.merge_range(table_row, 3, table_row, 9,'An entity that has been provided to Metra by the Sold-to party, where the Sold-to party has informed Metra that they intend to resell the goods to it. It is mandatory that the Sold-to party doesn’t resell the goods to any party other than the end-user intended. ', format_5)
            table_row += 2




            sheet.merge_range(table_row, 0, table_row, 9,'2. Quotations/Orders/Contract', format_6)
            table_row += 1
            text_term_2='''Quotations are only valid in writing and during the period that they state. If unstated, the period is 3 days. Please check the Order Confirmation and notify Metra of any mistake in writing immediately or the details stated in the Order confirmation will apply to this Agreement. All Products and pricing information is based on latest information available. Subject to change without notice or obligation. 
The Customer cannot cancel or change a Purchase Order(s) or Order Confirmation sent to Metra. The Customer(s) are obliged to accept the deliveries within (2) calendar days from the time the Products are made available at the place of delivery stated in the order confirmation. If the Customer refuses or delays delivery without Metra's agreement, the Customer must pay Metra's expenses or loss resulting from that refusal, including storage costs, until the Customer accepts delivery. Nothing in this agreement affects Metra's right to cancel or reject any order at any time
'''
            sheet.merge_range(table_row, 0, table_row, 9,text_term_2, format_5)
            table_row += 2
            sheet.merge_range(table_row, 0, table_row, 9,'3. Pricing', format_6)
            table_row += 1
            text_term_3='''Products offering prices, tax, shipment, insurance and installation are as shown on the invoice. Changes to exchange rates, duties, insurance, freight, market condition, and purchase costs (incl. for components and services) may cause Metra to adjust prices accordingly.

'''
            sheet.merge_range(table_row, 0, table_row, 9,text_term_3, format_5)
            table_row += 2
            sheet.merge_range(table_row, 0, table_row, 9,'4. Payment Terms & Payment Obligation', format_6)
            table_row += 1
            text_term_4_1='''Payment will be made as agreed in writing by Metra or in absence of such agreement, the payment is due immediately, without further notice from Metra. Payment timing is of the essence. Metra may suspend deliveries or service until full payment for that order. In case of delay in payment, Metra and the Customer agree that the Customer shall pay Metra liquidated damages in an amount equivalent to 2% monthly accruing on a day-to-day basis for each day of late payment (unless we otherwise elect) on the overdue amount, and the costs of recovery shall be payable by the Customer. 
The Customer agrees that all invoices and any other amounts due under this agreement are payable solely to us in the currency of payment stated above, in full without any set off, counter-claims, abatement, or reduction. We may at our sole discretion apply payments made to us (whether by the Customer or otherwise) to pay late payment charges, invoices overdue interest, or any outstanding amounts. The Customer must pay all sums due to us under this agreement, including invoices and other charges in full, without abatement, discount, reduction, set off, dispute or counterclaim. The Customer will not assert against Metra any claims the Customer may have against any third party including the manufacturer or original supplier or shipper of the Products. We have no obligation to perform any obligation by any third party. Metra may set off against any amounts owed by Metra to the Customer any amounts due from the Customer to Metra (including those prospectively or contingently due where in our reasonable opinion they are likely to become payable). 
Metra may at any time and at its sole discretion cancel a Customer’s credit line. In case of cancellation of the credit line, all invoices become immediately due.
Advance payments are due on the contract date and are non-refundable. Metra reserves the right to settle advance payments against any other due amounts, including but not limited to finance charges, holding fees or any other dues.
If the Customer is purchasing the Products from Metra’s subsidiary in Egypt (Metra Computers S.A.E) it shall have the right to select the currency in which the order shall be paid, hereinafter referred to as the “payment currency”, at the time of receiving the quotation from Metra. Metra shall have the right to give different prices depending on the payment currency. If a Customer selects payment in a foreign currency (not Egyptian Pounds), then the Customer must pay in the foreign currency as specified in the contract of sale. If a Customer selects payment in local currency (Egyptian Pounds), then Customer must pay at the higher of, the rate declared by the Central Bank of Egypt or any local Egyptian bank on the date of payment or due date of invoice (whichever is higher).
'''
         
            sheet.merge_range(table_row, 0, table_row, 9,text_term_4_1, format_5)
            table_row += 2

          

            sheet.merge_range(table_row, 0, table_row, 9,'5. Fair Pricing', format_6)
            table_row += 1
            text_term_5_1='''Subject to the compliance with anti-trust laws, where Metra discloses to the Customer a special discount for a specific End-User, the Customer acknowledges and certifies that the full amount of the discount reflected in Metra’s offer is necessary for the Customer to close any corresponding transactions with End-User, either directly or through a reseller. Accordingly, the Customer is responsible for ensuring that the End-User receives the entire financial benefit of the discount reflected in Metra’s offer. Metra will provide an Estimated End User Price (“EEP”) which will be Metra’s estimate of the highest price that End-User could pay while also receiving the entire benefit of the discount. While the Customer has the exclusive right to determine their own sales prices for Metra’s Products(s), the Customer must comply with the foregoing obligation to pass down the financial benefit of the discount to the End-User.  

'''
         
            sheet.merge_range(table_row, 0, table_row, 9,text_term_5_1, format_5)
            table_row += 2
         
            sheet.merge_range(table_row, 0, table_row, 9,'6. Delivery/Title/Risk', format_6)
            table_row += 1
            tetx_term_6_1='''The Delivery period in the Order confirmation is approximate and based solely on estimates. Any failure to comply with such dates shall not constitute a breach of contract by Metra. If no dates are specified, delivery will occur within a reasonable timeframe, considering the standard delivery duration for those specific Products from the manufacturer concerned. Handover of Products will take place within a reasonable timeframe following their delivery from the manufacturer, accounting for the typical duration required for arranging and executing shipping to the designated handover location, as well as completing any necessary formalities. Metra shall not be liable for any delays in delivery caused by the manufacturer of the Products. 
Partial deliveries may be made. The place of delivery is stated in the Order confirmation. Title to Products passes on full payment and until then the Customer must insure the Products and the Customer must not modify or pledge them. The Customer may use the Products, without modification, in the ordinary course of business. Metra reserves the rights to enter the storage premises to repossess the Products. If the Customer sells them before title passes, the Customer will become Metra's agent and the proceeds of such sale shall be held on Metra's behalf separately from the Customer's general funds. Metra may sue for the Price before title passes. All risk of the loss of the Products passes to the Customer upon delivery. 
The Customer acknowledges and understands that any of Metra’s affiliates or subsidiaries may provide the Customer with the Products.
Upon receiving the Products, the Customer or the Ship-to party must sign the delivery note. Any missing or damaged packaging should be noted on the delivery note prior to signing it by the Customer or the Ship-to party. Metra shall be entitled to assume that any person who both reasonably appears and claims to have authority to accept delivery who signs a note in respect of the Products on behalf of the Customer or the End-User (if Metra has agreed to deliver direct) does in fact have the authority.
Customer understands and agrees that Metra may accept an order therefrom but such order might not be released for delivery if the Customer has any debts or overdue payments to Metra. It is the Customer’s responsibility to ensure that it is within credit limit and has no overdue invoices in order for an order to be released for delivery by Metra.
The Customer undertakes not to sell the Products purchased from Metra to any party other than the End-user intended and previously declared to Metra.
'''
          
            sheet.merge_range(table_row, 0, table_row, 9,tetx_term_6_1, format_5)
            table_row += 2
          

            sheet.merge_range(table_row, 0, table_row, 9,'7. Service/ Software Orders', format_6)
            table_row += 1
            text_term_7_1='''Any item in an order which relates to a service/training which is to be provided by the Original Equipment Manufacturer (“OEM”) is the sole responsibility of the respective OEM. Metra’s role for such services/training is limited to procuring the same from the respective OEM as a part number and invoicing the same part number to Customer without any obligation on Metra for services being rendered by the respective OEM. Not rendering of services in a timely manner by any OEM will not entitle Customer to hold any payments of Metra. A service/software will be deemed accepted by the Customer once the OEM or Metra issues an invoice pertaining to the ordered service/software. Upon issuance of the invoice from Metra to the Customer, the Customer is obliged to pay for the ordered service/software on the due date mentioned on the invoice. 
'''
          
            sheet.merge_range(table_row, 0, table_row, 9,text_term_7_1, format_5)
            table_row += 2
          

            sheet.merge_range(table_row, 0, table_row, 9,'8. Holding Fees', format_6)
            table_row += 1
            tetx_term_8='''Customer hereby acknowledges and agrees that Metra shall charge a holding fee up to 2% per month, on Products where Customer causes a delay in acceptance of the delivery and/or collection of the Products from Metra. It is the Customer’s responsibility to ensure that it is within credit limit and has no overdue invoices in order for an order to be released for delivery by Metra. The holding fee shall accrue on a daily basis, and shall be calculated upon any delay more than one (1) week. It is the Customer's sole responsibility to ensure the existence of a sufficient credit line with no overdue payments to Metra, or alternatively that the Customer pays all necessary amounts to Metra to ensure that the Products can be delivered to the Customer. 
'''
            sheet.merge_range(table_row, 0, table_row, 9,tetx_term_8, format_5)
            table_row += 2
            sheet.merge_range(table_row, 0, table_row, 9,'9. Acceptance and Returns', format_6)
            table_row += 1
            tetx_term_9='''The Ship-to Party must inspect the Products upon receiving them from Metra, for any defects or non-conformity, and if any, the Ship-to party must notify Metra immediately and mention any discrepancies on the proof of delivery. After this, the Ship-to party and the Customer will have accepted the Products. If Metra agrees to the return of Products at its choosing, it must be in its original condition with packaging, a return note and proof of purchase.
To the greatest extent permitted under applicable law, any warranty from Metra in relation to defects in the Products sold by Metra (including warranty for defects in materials, workmanship, merchantability, or fitness for a particular use, or any other warranty) is hereby expressly excluded, unless otherwise accepted by Metra in writing. To the extent that the vendor or manufacturer of the Products provide separate warranties for the benefit of the Customer or the End-User, then such persons may enforce such vendor and/or manufacturer warranties in accordance with the terms and conditions applicable to them, at no cost or liability for Metra.
'''
            sheet.merge_range(table_row, 0, table_row, 9,tetx_term_9, format_5)
            table_row += 2

            sheet.merge_range(table_row, 0, table_row, 9,'10. Trade and Import Authorizations', format_6)
            table_row += 1
            tetx_term_10='''The Customer hereby warrants and represents that the Customer has and shall continue to have the due authorizations and licenses necessary and required to purchase the Products and any other Products purchased from Metra and to import the same into the relevant country. Any failure by the Customer to clear the Products from the relevant customs or other authorities in the relevant country whether due to the failure to obtain or maintain the requisite authorizations or licenses or for any other reason whatsoever, will not invalidate this Agreement and the Customer shall remain bound by the terms of this Agreement, including liability to make payments to Metra under the terms of this Agreement.
'''
            sheet.merge_range(table_row, 0, table_row, 9,tetx_term_10, format_5)
            table_row += 2

            sheet.merge_range(table_row, 0, table_row, 9,'11. Export Control', format_6)
            table_row += 1
            tetx_term_11_1='''The Customer acknowledges that Products(s) may include technology and Software which is subject to US and EU export control laws and laws of the country where it is delivered or used: the Customer must abide by all these laws. Products may not be sold, leased or transferred to restricted / embargoed end users, or countries, or for a user involved in weapons of mass destruction or genocide, without the prior consent of the US or competent EU government. The Customer understands and acknowledges that US and EU restrictions vary regularly and depending on Products, therefore the Customer must refer to the most current US and EU regulations.
'''
           
            sheet.merge_range(table_row, 0, table_row, 9,tetx_term_11_1, format_5)
            table_row += 2
          

            sheet.merge_range(table_row, 0, table_row, 9,'12. Foreign Corrupt Practices Act ("FCPA")', format_6)
            table_row += 1
            tetx_term_12='''Each Party shall comply with all applicable laws and regulations enacted to combat bribery and corruption, including the United States Foreign Corrupt Practices Act ("FCPA"), the local Bribery Acts, the principles of the OECD Convention on Combating Bribery of Foreign Public Officials (the "OECD Convention"), and any corresponding laws of all countries where business or services will be conducted or performed, pursuant to this Agreement. Each Party (including its directors, administrators, officers, representatives) shall not, directly or indirectly through a third party, pay, offer, promise to pay, or give anything of value to any person, including an employee or official of a government, government controlled enterprise or company, vendor, Customer, or political party, with the reasonable knowledge that it will be used for the purpose of obtaining any improper benefit or to improperly influence any act or decision by such person or party for the purpose of obtaining, retaining, or directing business.
'''
            sheet.merge_range(table_row, 0, table_row, 9,tetx_term_12, format_5)
            table_row += 2

            sheet.merge_range(table_row, 0, table_row, 9,'13. Right of Review and Audit', format_6)
            table_row += 1
            tetx_term_13_1='''Metra’s vendors shall have the right to review and audit, upon written request and during the normal business hours, Customer’s processes, books, records and accounting practices involving transactions related to this Agreement and to any relevant Agreement where Metra is the supplier of the Products.
Upon notice from Metra, the Customer shall provide Metra’s vendors and/or any representative designated by Metra’s vendors, with access to and any assistance that may be required for the purpose of performing audits or inspection of the services and the business of the Customer relating to this Agreement or any relevant Agreement. If the Customer is notified of not being in compliance to any law or audit requirement by an auditor designated by Metra’s vendors, the Customer shall promptly take action to comply with such requirements and shall bear all the cost incurred for any such compliance.
Customer understands and agrees that Metra shall have the right to disclose Customer’s records to its vendors, and this shall not be deemed as a breach of confidentiality by Metra.
'''
           
            sheet.merge_range(table_row, 0, table_row, 9,tetx_term_13_1, format_5)
           
            table_row += 2

            sheet.merge_range(table_row, 0, table_row, 9,'14. Assignment', format_6)
            table_row += 1
            tetx_term_14_1='''Metra shall at all times have the right to assign any receivables, rights and/or obligations arising from this Agreement. The Customer hereby acknowledges and accepts such assignment.
'''
           
            sheet.merge_range(table_row, 0, table_row, 9,tetx_term_14_1, format_5)
           
            table_row += 2

            sheet.merge_range(table_row, 0, table_row, 9,'15. Communication & Confidentiality', format_6)
            table_row += 1
            tetx_term_15_1='''Metra shall not be responsible for any communication made with its employees via email, phone, fax, or SMS regarding credit notes, discounts, or purchase commitments. Only formal credit notes, purchase orders, or contracts issued by Metra shall be considered valid.
Each party must treat all information received from the other marked "confidential" or reasonably obvious to be confidential as it would treat its own confidential information. 
'''
      
            sheet.merge_range(table_row, 0, table_row, 9,tetx_term_15_1, format_5)
            
            table_row += 2

            sheet.merge_range(table_row, 0, table_row, 9,'16. Governing Law', format_6)
            table_row += 1
            tetx_term_16_1='''These terms and all disputes in connection with these terms are governed by the substantive laws in force in the country in which the Metra billing entity is domiciled, without regard to its conflict of law rules; and the exclusive place of jurisdiction for any dispute will be in that country. In any event, neither the U.N. Convention on Contracts for the International Sale of Goods, nor the Uniform Computer Information Transaction Act will apply to these terms or any dispute.
'''
      
            sheet.merge_range(table_row, 0, table_row, 9,tetx_term_16_1, format_5)
            
            table_row += 2
            sheet.merge_range(table_row, 0, table_row, 9,'17. Digital Acceptance', format_6)
            table_row += 1
            tetx_term_17_1='''The Customer agrees that any contract, agreement, or document requiring signatures, including this Agreement, may be executed electronically. Electronic signatures and digital copies hold the same legal validity as traditional ink signatures. Additionally, submissions via 'submit' buttons or similar electronic means are deemed valid and binding. The Customer agrees not to contest the validity of electronically executed documents. 
'''
      
            sheet.merge_range(table_row, 0, table_row, 9,tetx_term_17_1, format_5)
            
            table_row += 2
            

            tetx_sign='''The signature below represents the Customer’s acknowledgement and acceptance of the order/quotation from Metra, which shall be governed by the terms set forth above. 
'''
      
            sheet.merge_range(table_row, 0, table_row, 9,tetx_sign, format_5)
            
            table_row += 2

            sheet.merge_range(table_row, 0, table_row, 1,'Signature:', format_5)
            if obj.signature:
                sign_image = io.BytesIO(base64.b64decode(obj.signature))
                sheet.insert_image(table_row,2,"image.png",{'image_data':sign_image,'x_scale':0.3,'y_scale':0.1})
            
            table_row += 5
            sheet.merge_range(table_row, 0, table_row, 1,'Customer Name:', format_5)
            sheet.merge_range(table_row, 2, table_row, 9,obj.partner_id.name, )
            
            table_row += 2
            sheet.merge_range(table_row, 0, table_row, 1,'Date:', format_5)
            sheet.merge_range(table_row, 2, table_row, 9,obj.signed_on,date_format)
            
            table_row += 2
            




    

      



