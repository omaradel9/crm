# -*- coding: utf-8 -*-
# from odoo import http


# class SaleQuoteMail(http.Controller):
#     @http.route('/sale_quote_mail/sale_quote_mail', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sale_quote_mail/sale_quote_mail/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('sale_quote_mail.listing', {
#             'root': '/sale_quote_mail/sale_quote_mail',
#             'objects': http.request.env['sale_quote_mail.sale_quote_mail'].search([]),
#         })

#     @http.route('/sale_quote_mail/sale_quote_mail/objects/<model("sale_quote_mail.sale_quote_mail"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sale_quote_mail.object', {
#             'object': obj
#         })
