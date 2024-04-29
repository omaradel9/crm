# -*- coding: utf-8 -*-
from odoo import http, _
from odoo.http import request
import logging
_logger = logging.getLogger(__name__)

class SaleQuoteMail(http.Controller):
    @http.route('/sale/update/po_no', type='json', auth='public')
    def po_no(self, **kw):
        po_no = kw.get('po_no')
        sale_id = kw.get('sale_id')
        if po_no:
            sale_order = request.env['sale.order'].sudo().search([('id', '=',sale_id)])
            sale_order.write({'po_no':str(po_no)})
            return po_no

