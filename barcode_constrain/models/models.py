# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ProductProduct(models.Model):
    _inherit = "product.template"
    alt_barcode = fields.Char(
        'EAN Code', copy=False, index='btree_not_null',
        help="International Article Number used for product identification.")
