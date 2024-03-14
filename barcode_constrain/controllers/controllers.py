# -*- coding: utf-8 -*-
# from odoo import http


# class BarcodeConstrain(http.Controller):
#     @http.route('/barcode_constrain/barcode_constrain', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/barcode_constrain/barcode_constrain/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('barcode_constrain.listing', {
#             'root': '/barcode_constrain/barcode_constrain',
#             'objects': http.request.env['barcode_constrain.barcode_constrain'].search([]),
#         })

#     @http.route('/barcode_constrain/barcode_constrain/objects/<model("barcode_constrain.barcode_constrain"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('barcode_constrain.object', {
#             'object': obj
#         })
