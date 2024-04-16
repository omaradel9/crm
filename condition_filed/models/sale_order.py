from odoo import fields, models, api
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = 'sale.order'






    def _check_duration_visiblity(self):
        # see if the duration is number and not equle to zero make the field 
        # visible in the reports
        
        duration_values = []

        for line in self.order_line:
            if isinstance(line.duration, str):
                try:
                    duration = int(line.duration)
                except ValueError:
                    raise ValidationError('Service Duration Must Be Number Not String')
                else:
                    if duration != 0:
                        duration_values.append(duration)
        
        return duration_values               



