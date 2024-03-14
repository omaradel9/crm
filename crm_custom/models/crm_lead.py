from odoo import api,  fields, models, _, Command



class CrmLead(models.Model):
    _inherit = "crm.lead"


    per_sales_person = fields.Many2one('res.users', string="PreSalesperson")

    deal_type = fields.Selection(
        string='Deal Type',
        selection=[('fulfilment', 'Fulfilment'), ('incremental', 'Incremental')],
        help="Type is used to separate Fulfilment and Incremental")
    
    line_business_id = fields.Many2one(
        string='Business Line',
        comodel_name='crm.line.business',
        ondelete='restrict',
    )
    
   
    
    expected_revenue = fields.Monetary('Expected Revenue', currency_field='related_currency', tracking=True)
    recurring_revenue = fields.Monetary('Recurring Revenues', currency_field='related_currency', tracking=True)

    
   

  



    price_list_crm_id = fields.Many2one(
        string='Currency',
        comodel_name='product.pricelist',
        ondelete='restrict',
        required=True
    )

    related_currency = fields.Many2one(
        string='Currency',
        comodel_name='res.currency',
        compute='_compute_related_currency',
        store=True,
    )

    @api.depends('price_list_crm_id')
    def _compute_related_currency(self):
        for record in self:
            record.related_currency = record.price_list_crm_id.currency_id.id
    

    