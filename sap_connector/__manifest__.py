# -*- coding: utf-8 -*-
{
    'name': "SAP connector",

   

    'description': """
    
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','sale','quotation_dublicate','modify_modules'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/res_partner_view.xml',
        'views/sale_order.xml',
        'wizard/sap_id_wizard.xml',
        'wizard/set_default_code_view.xml',
        'wizard/set_payment_note.xml',
     
    ],
    'sequence':'-1',
    'installable': True,
    'application': True,
  
}
