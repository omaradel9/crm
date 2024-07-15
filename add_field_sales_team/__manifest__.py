# -*- coding: utf-8 -*-
{
    'name': "field sales team ",

   

    'description': """
        add fields in company, product, sales team models
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','product','sales_team','company_empty_file_field','sale','crm_kanban_view'],

    # always loaded
    'data': [
        'security/ir_rule.xml',
        'views/res_company_view.xml',
        'views/product_template_view.xml',
        'views/sales_team_view.xml',
        'views/sale_order_wizard.xml',
        'views/sale_order_view.xml'
    ],
  
}
