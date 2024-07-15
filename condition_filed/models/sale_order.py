from odoo import fields, models, api
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    import_lines_types = fields.Selection([('update_lines', 'Update Lines'), ('add_lines', 'Add Lines')],
                                          default="update_lines", string='Import Lines Type')






    def _check_duration_visiblity(self):
        # see if the duration is number and not equle to zero make the field 
        # visible in the reports
        
        duration_values = []

        for line in self.order_line:
            if isinstance(line.duration, str):
                try:
                    duration = int(line.duration)
                except ValueError:
                    line.duration = False

                else:
                    if duration != 0:
                        duration_values.append(duration)
                    elif duration == 0:
                        line.duration = False
        
        return duration_values 
    
    



