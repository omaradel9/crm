{
    "name": "Company Empty File",
    "description": "make the downloaded empty file get from field in the company rather than add it as static  ",
    "author": "Basant Gaber Abd-Elaziz",
    "data": [
        'views/res_company_view.xml',
        'views/sale_order_view.xml',
    
     
        
   
        
       

    ],
    'sequence':'-1',
    "depends": ["base","download_empty_file_sale_lines","condition_filed","hide_download_order_line"],

    'installable': True,
    'application': True,





    
   

   
    
    
  
  
}