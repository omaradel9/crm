# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class sale_quote_mail(models.Model):
#     _name = 'sale_quote_mail.sale_quote_mail'
#     _description = 'sale_quote_mail.sale_quote_mail'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
