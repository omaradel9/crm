{
    "name": "Send By Email",
    "description": "change the send by email attachment by the custom pdf report",
    "author": "Metra",
    "depends": ["base", "sale","sale_order_reports"],
    "data": [
        'data/mail_template_data.xml',
        'views/sale_order_view.xml',
        'views/template.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'send_by_email/static/**/*',
        ]
    },
    'sequence':'-1',

    'installable': True,
    'application': True,





    
   

   
    
    
  
  
}