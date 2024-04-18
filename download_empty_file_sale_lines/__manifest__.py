{
    "name": "download empty file",
    "description": "download empty sample file to use when importing in the  sales order lines, and make all the custom field in the sale order line optional",
    "author": "Basant Gaber Abd-Elaziz",
    "data": [
        'data/attachment_file.xml',
        'views/sale_order.xml'
      
    
     
        
   
        
       

    ],
    'sequence':'-1',
    "depends": ["base","import_order_lines","condition_filed"],

    'installable': True,
    'application': True,



  


    
   

   
    
    
  
  
}