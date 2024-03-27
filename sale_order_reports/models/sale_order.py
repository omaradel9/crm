from odoo import models, api, fields



class SaleOrder(models.Model):
    _inherit = "sale.order"




    
    brand_id = fields.Many2one(
        string='Usage',
        comodel_name='brand',
        ondelete='restrict',
    )

    term_conditions_id= fields.Many2one(
        comodel_name='terms.condtions.sales',
        ondelete='restrict',
    )

    end_user_id = fields.Many2one(
        string='End User',
        comodel_name='res.partner',
        ondelete='restrict',
    )


  


  






  

    
    
    
    
    