# -*- coding: utf-8 -*-
{
    'name': "SAP Feedback",

   

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
    'depends': ['base','sale','edit_sales_reports','add_field_sales_team','sap_connector','web'],

    # always loaded
    'data': [
        'views/sale_order_view.xml',
        'views/webclient_template.xml',
     
     
    ],
    'assets':{
     
        'web.assets_frontend': [
            'sap_feedback_page/static/src/scss/contact_btn.scss'

                     ]
    },
     
    'sequence':'-1',
    'installable': True,
    'application': True,
  
}