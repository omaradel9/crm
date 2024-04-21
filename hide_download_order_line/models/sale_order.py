from odoo import fields,models,api



class SaleOrder(models.Model):
    _inherit="sale.order"




    
    import_lines_type = fields.Selection(
        string='Import Type',
        selection=[('add_lines', 'Add Lines'), ('update_lines', 'Update Lines')],
        help="Add Line: Will add new lines to the exsited ones,\n Update Lines: will remove the old lines and add new ones"
    )
    