odoo.define('send_by_email.sale_portal_js_custom', function (require) {
    "use strict";
    var ajax = require('web.ajax');

     function add_po_no() {
        let po_no = document.getElementById('po_no').value
        let sale_id = document.getElementById('sale_id').value
        console.log("=====document"+ po_no)
        ajax.jsonRpc("/sale/update/po_no", 'call', {
                'po_no': po_no,
                'sale_id': sale_id,
                }).then(function (data) {
                    console.log(data)
                })
           }
    $(document).on('keyup', "#po_no",add_po_no)

})