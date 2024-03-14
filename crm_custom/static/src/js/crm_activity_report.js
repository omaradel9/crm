odoo.define('crm_custom.crm_create_activity_button', function (require) {
    "use strict";
    var ListController = require('web.ListController');
    var ListView = require('web.ListView');
    var viewRegistry = require('web.view_registry');
    var TreeButton = ListController.extend({
       buttons_template: 'crm_button_custom.buttons',
       events: _.extend({}, ListController.prototype.events, {
           'click .open_wizard_action': '_OpenWizard',
       }),
       _OpenWizard: function () {
           var self = this;
            this.do_action({
               type: 'ir.actions.act_window',
               res_model: 'activity.report.create.wizard',
               name :'Open Wizard',
               view_mode: 'form',
               view_type: 'form',
               views: [[false, 'form']],
               target: 'new',
               res_id: false,
           });
       },
       renderButtons: function () {
        var self= this;
        this._super.apply(this, arguments);
        this.getSession().user_has_group('crm_custom.group_validate').then(function (hasGroup) {
                if (!hasGroup) {
                    self.$buttons.find('.open_wizard_action').addClass('d-none');
                }
            });
        },

    });
    var CrmActivityListView = ListView.extend({
       config: _.extend({}, ListView.prototype.config, {
           Controller: TreeButton,
       }),
    });
    viewRegistry.add('button_in_tree', CrmActivityListView);
    });