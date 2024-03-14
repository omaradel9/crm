{
    "name": "CRM Custom",
    "description": "edition for the crm module",
    "author": "Basant Gaber Abd-Elaziz",
    "data": [
        'security/access_right.xml',
        'security/crm_group.xml',
        'views/crm_activity_report_views.xml',
        'wizard/crm_activity_report_edit_wizard.xml',
        'wizard/crm_activity_report_create_wizard.xml',
        'views/crm_planned_activity_view.xml',
        'views/res_config_settings_view.xml',
        'views/sale_order_view.xml',
        'views/crm_attachment.xml',
        'views/mail_message.xml',
        'views/crm_lead_view.xml',
     
        
   
        
       

    ],
    'sequence':'-1',
    "depends": ["base","crm","web","sale"],

    'installable': True,
    'application': True,



    'assets':{
        'web.assets_backend':[
            
            '/crm_custom/static/src/js/crm_activity_report.js',
            '/crm_custom/static/src/xml/crm_activity_report.xml',
            
        ]
    }


    
   

   
    
    
  
  
}

