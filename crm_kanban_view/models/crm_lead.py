from odoo import fields,models,api



class CrmLead(models.Model):
    _inherit="crm.lead"


    
    end_user_id = fields.Many2one(
        string='End User',
        comodel_name='res.partner',
        ondelete='restrict',
    )
    partner_id = fields.Many2one(
        'res.partner', string='Customer', check_company=True, index=True, tracking=10,
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id),('parent_id','=', False)]",
        help="Linked partner (optional). Usually created when converting the lead. You can find a partner by its Name, TIN, Email or Internal Reference.")

    vendor_id = fields.Many2one('res.partner', string='Vendor',domain="[('parent_id','=', False)]", ondelete='restrict',)

   

    contact_person = fields.Many2one('res.partner',string="Contact Person")



    @api.onchange('partner_id')
    def _get_contact_person(self):
        if self.contact_person.parent_id.id != self.partner_id.id:
               self.contact_person=False
    

    







    def _prepare_opportunity_quotation_context(self):
        """ Prepares the context for a new quotation (sale.order) by sharing the values of common fields """


        res = super(CrmLead, self)._prepare_opportunity_quotation_context()
        if self.end_user_id:
            res['default_end_user_id'] = self.end_user_id.id
        if self.vendor_id:
            res['default_vendor_id'] = self.vendor_id.id 
        if self.contact_person:
            res['default_contact_person'] = self.contact_person.id    



        return res 
    


  


    @api.depends(lambda self: ['stage_id', 'team_id'] + self._pls_get_safe_fields())
    def _compute_probabilities(self):
        lead_probabilities = self._pls_get_naive_bayes_probabilities()
        for lead in self:
            if lead.stage_id:
                lead.probability = lead.stage_id.probability
               


            elif lead.id in lead_probabilities:
                was_automated = lead.active and lead.is_automated_probability
                lead.automated_probability = lead_probabilities[lead.id]
                if was_automated:
                    lead.probability = lead.automated_probability     


      

       
    












