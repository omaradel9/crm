from odoo import models, api, fields



class saleOrder(models.Model):
    _inherit = "sale.order"



   
    
    parent_porposal_id = fields.Many2one(
        string='Parent Proposal',
        comodel_name='sale.order',
        ondelete='restrict',
        readonly=True
    )

    
 
    
    dublicated_counter = fields.Integer()


    def action_preview_dublicated_quotation(self):
        return {
                'name':'Versions',
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'sale.order',
                'target': 'current',
                'domain': [('parent_porposal_id','=', self.id)],
                }
        






    def action_dublicate_quotation(self):
        
        if self.parent_porposal_id:
            counter = self.parent_porposal_id.dublicated_counter + 1
            dublicated_record = self.copy()
            self.parent_porposal_id.write({
                'dublicated_counter':counter,

            })

            
            dublicated_record.write({
                'dublicated_counter':0,
                'parent_porposal_id': self.parent_porposal_id.id,
                'name':f'{self.parent_porposal_id.name}-V {counter}'
            })
        else:
            self.dublicated_counter+=1
            dublicated_record = self.copy()
           
           
            dublicated_record.write({
                'parent_porposal_id': self.id,
                'name':f'{self.name}-V {self.dublicated_counter}'
            })


        return {
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'sale.order',
                'target': 'current',
                'res_id': dublicated_record.id,
                'view_id': self.env.ref('sale.view_order_form').id,
                }
        