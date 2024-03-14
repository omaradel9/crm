from odoo import models, api, fields



class Brand(models.Model):
    _name = "brand"
    
    
    
    name = fields.Char(string="Brand Name")
    image = fields.Binary(string="Brand Image")

    
   
    
    


   