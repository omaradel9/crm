from odoo import  models, _
from odoo.exceptions import ValidationError



class QuotationReportXlsx(models.AbstractModel):
    _inherit = 'report.import_order_lines.custom_import_line_report_xlsx'






    def generate_xlsx_report(self, workbook, data, orders):
        format_1 = workbook.add_format({'bold': True, 'align': 'center', 'valign': 'vcenter', 'bg_color': '#cccccc'})
        bold = workbook.add_format({'bold': True,'valign': 'vcenter'})

        sheet = workbook.add_worksheet('Import Sale Order Lines')
        sheet.set_row(0, 40)
        sheet.set_column(0, 20, 30)
       


        col =0
        order_id = self.env['sale.order'].search([('id', '=', data['order_id'])])

        company_id = self.env['res.company'].search([('id', '=',self.env.company.id)])

        duration_values = []

        for line in order_id.order_line:
            if isinstance(line.duration, str):
                try:
                    duration = int(line.duration)
                except ValueError:
                    line.duration = False

                else:
                    if duration != 0:
                        duration_values.append(duration)
                    elif duration == 0:
                        line.duration = False    


       



        

      
            

       
        sheet.write(0, col, 'Line Number', format_1)
        col += 1
        sheet.write(0, col, 'MPN', format_1)
        col += 1
        sheet.write(0, col, 'Smart Account Mandatory', format_1)
        col += 1
        sheet.write(0, col, 'Product Description', format_1)
        col += 1
        sheet.write(0, col, 'Vendor Product Reference', format_1)
        col += 1
        sheet.write(0, col, 'Product Family / Service Level', format_1)
        col += 1
        if order_id:
            if duration_values:
                sheet.write(0, col, 'Service Duration (Months)', format_1)
                col += 1    
        else:
            sheet.write(0, col, 'Service Duration (Months)', format_1)
            col += 1

             
    
                
        sheet.write(0, col, 'Estimated Lead Time (Days)', format_1)
        col += 1
        sheet.write(0, col, 'Unit Vendor List Price', format_1)
        col += 1
        sheet.write(0, col, 'Pricing Term', format_1)
        col += 1
        sheet.write(0, col, 'Quantity', format_1)
        col += 1
        sheet.write(0, col, 'Unit Net Price', format_1)
        col += 1
        sheet.write(0, col, 'Vendor Discount (%)', format_1)
        col += 1
        sheet.write(0, col, 'Total Price', format_1)
        col += 1
        sheet.write(0, col, 'Partner Unit Net Price', format_1)
        col += 1
        sheet.write(0, col, 'Partner Discount (%)', format_1)
        col += 1
        sheet.write(0, col, 'Conditions (%)', format_1)
        col += 1
        sheet.write(0, col, 'Margin (%)', format_1)
        col += 1
       
        sheet.write(0, col, 'Unit Selling Price', format_1)
        col += 1
        sheet.write(0, col, 'Total Selling Price', format_1)
        

        if data['order_id']:
         
     
                 
           

            
            for index, line in enumerate(order_id.order_line):
               
                    if line.display_type == 'line_section':
                        sheet.merge_range(index+1,0,index+1,19, line.name,bold)
                    elif line.display_type == 'line_note':
                        sheet.merge_range(index+1,0,index+1,19, line.name,bold)    
                    else: 
                        if duration_values: 
                            sheet.write(index+1, 0, line.line_number or index+1)  
                            sheet.write(index+1, 1, line.product_template_id.name)
                            sheet.write(index+1, 2, line.smart_account_mandatory or "--")
                            sheet.write(index+1, 3, line.name)
                            sheet.write(index+1, 4, line.cisco_product_ref or "--")
                            sheet.write(index+1, 5, line.product_family or "--")
                            sheet.write(index+1, 6, line.duration or 'N/A')
                            sheet.write(index+1, 7, line.estimated_lead_time or 'N/A')
                            sheet.write(index+1, 8, line.cost)
                            sheet.write(index+1, 9, line.pricing_term or "--")
                            sheet.write(index+1, 10, line.product_uom_qty)
                            row_num = index+2
                            sheet.write_formula(index+1, 11, f'=ROUND(I{row_num}-(I{row_num}*(M{row_num}/100)),2)')
                            sheet.write(index+1, 12, line.discount_metra)
                            sheet.write_formula(index+1, 13, f'=ROUND((K{row_num} * L{row_num}),2)')
                            sheet.write_formula(index+1, 14, f'=ROUND(I{row_num}-(I{row_num}*(P{row_num}/100)),2)')
                            sheet.write(index+1, 15, line.partner_discount)
                            sheet.write(index+1, 16, line.conditions)
                            sheet.write(index+1, 17, line.mergin)
                            sheet.write_formula(index+1, 18, f'=(L{row_num}*(1+Q{row_num}/100))/(1-R{row_num}/100)')
                            sheet.write_formula(index+1, 19, f'=S{row_num}*K{row_num}')
                          
                        else:
                            sheet.write(index+1, 0, line.line_number or index+1)  
                            sheet.write(index+1, 1, line.product_template_id.name)
                            sheet.write(index+1, 2, line.smart_account_mandatory or "--")
                            sheet.write(index+1, 3, line.name)
                            sheet.write(index+1, 4, line.cisco_product_ref or "--")
                            sheet.write(index+1, 5, line.product_family or "--")
                            sheet.write(index+1, 6, line.estimated_lead_time or 'N/A')
                            sheet.write(index+1, 7, line.cost)
                            sheet.write(index+1, 8, line.pricing_term or "--")
                            sheet.write(index+1, 9, line.product_uom_qty)
                            row_num = index+2
                            sheet.write_formula(index+1, 10, f'=ROUND(H{row_num}-(H{row_num}*(L{row_num}/100)),2)')

                            sheet.write(index+1, 11, line.discount_metra)
                            sheet.write_formula(index+1, 12, f'=ROUND((J{row_num} * K{row_num}),2)')
                            sheet.write_formula(index+1, 13, f'=ROUND(H{row_num}-(H{row_num}*(O{row_num}/100)),2)')
                            sheet.write(index+1, 14, line.partner_discount)
                            sheet.write(index+1, 15, line.conditions)
                            sheet.write(index+1, 16, line.mergin)
                            sheet.write_formula(index+1, 17, f'=(K{row_num}*(1+P{row_num}/100))/(1-Q{row_num}/100)')
                            sheet.write_formula(index+1, 18, f'=R{row_num}*J{row_num}')
                           

                
        else:
            pass 