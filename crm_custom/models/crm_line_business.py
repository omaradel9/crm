from odoo import fields, models, api


class CrmLineBusiness(models.Model):
    _name = "crm.line.business"



    name= fields.Char(string="Line Business")