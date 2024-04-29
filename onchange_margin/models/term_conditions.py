from odoo import fields,models,api


class TermsConditionsSales(models.Model):
    _inherit = "terms.condtions.sales"    



    company_id = fields.Many2one(
            comodel_name='res.company',
            required=True, index=True,
            default=lambda self: self.env.company)