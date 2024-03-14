from odoo import fields,models,api



class CrmLead(models.Model):
    _inherit="crm.lead"

    vendor_account_manager = fields.Many2one('res.partner',string="Vendor Account Manager")


    @api.onchange('vendor_id')
    def _get_vendor_account_manager(self):
        if self.vendor_account_manager.parent_id.id != self.vendor_id.id:
               self.vendor_account_manager=False



    def _prepare_opportunity_quotation_context(self):
        """ Prepares the context for a new quotation (sale.order) by sharing the values of common fields """


        res = super(CrmLead, self)._prepare_opportunity_quotation_context()
        if self.vendor_account_manager:
            res['default_vendor_account_manager'] = self.vendor_account_manager.id     



        return res            



