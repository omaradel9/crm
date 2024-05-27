from odoo import http
from odoo.http import request
from odoo.addons.web.controllers.main import content_disposition
import base64
from odoo.modules.module import get_resource_path

class Download_xls(http.Controller):
    
    @http.route('/web/binary/download_document', type='http', auth="public")
    def download_document(self, **kw):
    

         

    
        order_id = request.env['sale.order'].browse(int(kw['order_id']))
        filecontent = order_id.company_empty_file
        filename = 'MetraQuotationTemplateWithMacro.xlsm'
        de_filecontent = base64.b64decode(filecontent)

        return request.make_response(de_filecontent,
            [('Content-Type', 'application/octet-stream'),
            ('Content-Disposition', content_disposition(filename))])