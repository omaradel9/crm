from odoo import  models, _
import base64
import io
from odoo.modules.module import get_module_resource



class QuotationReportXlsx(models.AbstractModel):
    _inherit = 'report.import_order_lines.custom_import_line_report_xlsx'






    def generate_xlsx_report(self, workbook, data, orders):
        format_1 = workbook.add_format({'bold': True, 'align': 'center', 'valign': 'vcenter', 'bg_color': '#cccccc'})
        bold = workbook.add_format({'bold': True,'valign': 'vcenter'})

        sheet = workbook.add_worksheet('Import Sale Order Lines')
        sheet.set_row(0, 40)
        sheet.set_column(0, 0, 30)
        sheet.set_column(1, 1, 30)
        sheet.set_column(2, 2, 30)
        sheet.set_column(3, 3, 30)
        sheet.set_column(4, 4, 30)
        sheet.set_column(5, 5, 30)
        sheet.set_column(6, 6, 30)
        sheet.set_column(7, 7, 30)
        sheet.set_column(8, 8, 30)
        sheet.set_column(9, 9, 30)
        sheet.set_column(10, 10, 30)
        sheet.set_column(11, 11, 30)
        sheet.set_column(12, 12, 30)
        sheet.set_column(13, 13, 30)
        sheet.set_column(14, 14, 30)

        col =0
        order_id = self.env['sale.order'].search([('id', '=', data['order_id'])])

        company_id = self.env['res.company'].search([('id', '=',self.env.company.id)])



        

      
            

       
        sheet.write(0, col, 'Line Number', format_1)
        col += 1
        sheet.write(0, col, 'MPN', format_1)
        col += 1
        sheet.write(0, col, 'Smart Account Mandatory', format_1)
        col += 1
        sheet.write(0, col, 'Product Description', format_1)
        col += 1
        if company_id.brands =='cisco':
            sheet.write(0, col, 'Vendor Product Reference', format_1)
            col += 1
        sheet.write(0, col, 'Product Family / Service Level', format_1)
        col += 1
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
        sheet.write(0, col, 'Discount (%)', format_1)
        col += 1
        sheet.write(0, col, 'Total Price', format_1)

        if data['order_id']:
           

            
            for index, line in enumerate(order_id.order_line):
                if order_id.current_company_brands =='cisco':
                    if line.display_type == 'line_section':
                        sheet.merge_range(index+1,0,index+1,13, line.name,bold)
                    else:    
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
                        sheet.write(index+1, 11, line.price_unit)
                        sheet.write(index+1, 12, line.discount_metra)
                        sheet.write(index+1, 13, line.price_subtotal)
                else:
                    if line.display_type == 'line_section':
                        sheet.merge_range(index+1,0,index+1,12, line.name, bold)
                    else:    
                        sheet.write(index+1, 0, line.line_number or index+1)  
                        sheet.write(index+1, 1, line.product_template_id.name)
                        sheet.write(index+1, 2, line.smart_account_mandatory or "--")
                        sheet.write(index+1, 3, line.name)
                        sheet.write(index+1, 4, line.product_family or "--")
                        sheet.write(index+1, 5, line.duration or 'N/A')
                        sheet.write(index+1, 6, line.estimated_lead_time or 'N/A')
                        sheet.write(index+1, 7, line.cost)
                        sheet.write(index+1, 8, line.pricing_term or "--")
                        sheet.write(index+1, 9, line.product_uom_qty)
                        sheet.write(index+1, 10, line.price_unit)
                        sheet.write(index+1, 11, line.discount_metra)
                        sheet.write(index+1, 12, line.price_subtotal)    
        else:
            pass  