from odoo import fields,models,api



class ResPartner(models.Model):
    _inherit="res.partner"
    
    sap_id = fields.Char('SAP ID')
    
    
    @api.model
    def create(self, vals):
        res = super(ResPartner, self).create(vals)
        if res.parent_id and 'sap_id' in vals:
            res.sap_id = res.parent_id.sap_id
        return res

    def write(self, vals):
        res = super(ResPartner, self).write(vals)
        if 'sap_id' in vals:
            for partner in self:
                if partner.child_ids:
                    partner.child_ids.write({'sap_id': vals['sap_id']})
        return res
