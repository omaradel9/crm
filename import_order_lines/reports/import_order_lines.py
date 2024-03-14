from odoo import  models, _
import base64
import io
from odoo.modules.module import get_module_resource



class QuotationReportXlsx(models.AbstractModel):
    _name = 'report.import_order_lines.custom_import_line_report_xlsx'
    _inherit = 'report.report_xlsx.abstract'



    def generate_xlsx_report(self, workbook, data, orders):
        format_1 = workbook.add_format({'bold':True,'align': 'center'})

        sheet = workbook.add_worksheet('Import Sale Order Lines')
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

        col =0

       
        sheet.write(0, col,'Line Number', format_1)
        col+=1
        sheet.write(0, col,'Product Name', format_1)
        col+=1
        sheet.write(0, col,'Description', format_1)
        col+=1
        sheet.write(0, col,'Quantity', format_1)
        col+=1
        sheet.write(0, col,'Unit Price', format_1)
        col+=1
        sheet.write(0, col,'Duration', format_1)
        col+=1
        sheet.write(0, col,'Cost', format_1)
        col+=1
        sheet.write(0, col,'Taxs', format_1)
        col+=1
        sheet.write(0, col,'Metra Discount', format_1)
        col+=1
        sheet.write(0, col,'Special Discount', format_1)
        col+=1
        sheet.write(0, col,'Margin', format_1)


        if data['order_id']:
            
            order_id  = self.env['sale.order'].search([('id','=',data['order_id'])])
            for index, line in enumerate(order_id.order_line):
                sheet.write(index+1, 0, line.line_number)  
                sheet.write(index+1, 1, line.product_template_id.name)
                sheet.write(index+1, 2, line.name)
                sheet.write(index+1, 3, line.product_uom_qty)
                sheet.write(index+1, 4, line.price_unit)
                sheet.write(index+1, 5, line.duration)
                sheet.write(index+1, 6, line.cost)
                sheet.write(index+1, 7, line.tax_id.name)
                sheet.write(index+1, 8, line.discount_metra)
                sheet.write(index+1, 9, line.special_discount)
                sheet.write(index+1, 10, line.mergin)
                
               

        else:
            pass  


















  
           






      

        

    