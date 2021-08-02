odoo.define('customer_screen.pos_return',function(require){
"use strict";

var gui = require('point_of_sale.gui');
var chrome = require('point_of_sale.chrome');
var popups = require('point_of_sale.popups');
var rpc = require('web.rpc');
var core = require('web.core');
var PosBaseWidget = require('point_of_sale.BaseWidget');
var models = require('point_of_sale.models');
var pos_screens = require('point_of_sale.screens');
var BarcodeParser = require('barcodes.BarcodeParser');
var PosDB = require('point_of_sale.DB');
var devices = require('point_of_sale.devices');
var session = require('web.session');
var time = require('web.time');
var utils = require('web.utils');
var Mutex = utils.Mutex;
var round_di = utils.round_decimals;
var round_pr = utils.round_precision;
var Backbone = window.Backbone;
var PosModelSuper = models.PosModel;
var QWeb = core.qweb;
var _t = core._t;
var exports = {};
var pos_model = require('point_of_sale.models');



/*POS Order Data*/

//models.load_models({
//    model: 'pos.order',
//    fields: ['name','partner_id','state','amount_total', 'payment_status','delivery_status'],
//    loaded: function(self,orders){
//        self.orders = [];
//        for (var i = 0; i < orders.length; i++) {
//            self.orders[i] = orders[i];
//        }
//        console.log("posssss", self.orders)
//    },
//});

/*Sale Order Data*/

//models.load_models({
//    model: 'sale.order',
//    fields: ['id','name','date_order','amount_total','partner_id','lines','product_status','payment_status','delivery_status','team_id'],
//    loaded: function(self, sale_order){
//        self.squotations = [];
//        for(var quot=0;quot< sale_order.length;quot++){
//            self.squotations[quot] = sale_order[quot];
//        }
//        console.log("saleeee", self.squotations)
//    },
//});

/*Customer Payment Status*/
var ReturnButton = pos_screens.ActionButtonWidget.extend({
    template: 'ReturnButton',
    button_click: function(){
             this.gui.show_screen('ReturnOrdersWidget');
    },
});

pos_screens.define_action_button({
    'name': 'Return',
    'widget': ReturnButton,
    'condition': function(){
        return this.pos;
    },
});
//

var ReturnOrdersWidget = pos_screens.ScreenWidget.extend({
    template: 'ReturnOrdersWidget',

    init: function(parent, options){
        this._super(parent, options);
        this.order_string = "";
        var self = this;
        this.pos_reference = "";
        this.pos_place = "";

        var sale_order_data;
        var pos_order_data;

        rpc.query({
            model: 'pos.order',
            method: 'get_pos_order_data',
            args: [],
        }).then(function (result){
            if(result==0){
                console.log("NO POS DATA FOUND")
            }
            else{
                self.pos.db.pos_order_data = result;
            }
        });

        rpc.query({
            model: 'sale.order',
            method: 'get_sale_order_data',
            args: [],
        }).then(function (result){
            if(result==0){
                console.log("NO SALE DATA FOUND")
            }
            else{
                self.pos.db.sale_order_data = result;
            }
        });


    },

    auto_back: true,
    renderElement: function () {
        this._super(this);
        var self = this;

    },

    show: function(){
        var self = this;
        this._super();

        this.renderElement();
        this.details_visible = false;

        this.$('.back').click(function(){
            self.gui.back();
        });

        var pos_orders = this.pos.db.pos_order_data;
        var quotations = this.pos.db.sale_order_data;
        this.render_list(pos_orders,quotations,undefined);

        this.$('.order_search').keyup(function() {
            self.render_list(pos_orders,quotations,this.value);
        });

        this.$(".order_type").change(function(){
            console.log("nnbjxjnhbdfcv", $(this).val())
            var order_type = $(this).val();
            self.render_list(pos_orders,quotations,undefined, order_type);
        });
    },

    hide: function () {
        this._super();
        this.new_client = null;
    },

    get_order_by_id: function (id) {
        return this.pos.pos_orders[id];
    },

    render_list: function(orders,quotations,input_txt, order_type){

        var self = this;

        this.$('.order-list-lines').delegate('.return-button','click',function(event){
            var orderline = self.pos.get_order();
            var order = self.pos.get_order();
            var orderlines = self.pos.get_order().get_orderlines();
            var location = $(this).data('id');
            order.set_next(location);
            var locat = order.get_next();
            self.gui.show_screen('products');

        });

        if (order_type!='all'){
            if (order_type=='pos'){
                quotations = []
            }
            else if (order_type=='Mobile'||order_type=='Website'){
                orders=[]
                new_quotations = []
                for (var i = 0; i < quotations.length; i++) {
                    if (quotations[i].team_id[1]==order_type){
                        new_quotations = new_quotations.concat(quotations[i])
                    }

                }
                quotations = new_quotations
            }
        }

        if (input_txt != undefined && input_txt != '') {
            var new_order_data = [];
            var new_quotations = [];
            var search_text = input_txt.toLowerCase()

            for (var i = 0; i < orders.length; i++) {
                if (orders[i].partner_id == '') {
                    orders[i].partner_id = [0, '-'];
                }
//                if (((orders[i].name.toLowerCase()).indexOf(search_text) != -1) || ((orders[i].partner_id[1].toLowerCase()).indexOf(search_text) != -1)) {
                if (((orders[i].name.toLowerCase()).indexOf(search_text) != -1)) {
                    console.log("*****************")
                    new_order_data = new_order_data.concat(orders[i]);
                }

            }
            for (var i = 0; i < quotations.length; i++) {
                if (quotations[i].partner_id == '') {
                    quotations[i].partner_id = [0, '-'];
                }
//                if (((quotations[i].name.toLowerCase()).indexOf(search_text) != -1) || ((quotations[i].partner_id[1].toLowerCase()).indexOf(search_text) != -1)) {
                if (((quotations[i].name.toLowerCase()).indexOf(search_text) != -1)) {
                    new_order_data = new_order_data.concat(quotations[i]);
                }
            }
            orders = new_order_data;
            quotations = new_quotations;
        }

        var contents = this.$el[0].querySelector('.order-list-lines');
        if (contents){
            contents.innerHTML = "";
            for(var i = 0, len = Math.min(orders.length,1000); i < len; i++) {
                if (orders[i]) {
                    var order = orders[i];
                    var clientline_html = QWeb.render('OrderLines', {widget: this, order: order});
                    var orderline = document.createElement('tbody');
                    orderline.innerHTML = clientline_html;
                    orderline = orderline.childNodes[1];
                    contents.appendChild(orderline);
                }
            }
            for(var i = 0, len = Math.min(quotations.length,1000); i < len; i++) {
                if (quotations[i]) {
                    var order = quotations[i];
                    var clientline_html = QWeb.render('OrderLines', {widget: this, order: order});
                    var orderline = document.createElement('tbody');
                    orderline.innerHTML = clientline_html;
                    orderline = orderline.childNodes[1];
                    contents.appendChild(orderline);
                }
            }
        }
    },

    close: function(){
        this._super();
    },
});

gui.define_screen({name:'ReturnOrdersWidget', widget: ReturnOrdersWidget});

/*add customer details to pos.payment_status model*/
    pos_screens.ActionpadWidget.include({
        renderElement: function() {
            var self = this;
            this._super();
            this.$('.pay').click(function(){
                var order = self.pos.get_order();
                var client = order.get_client();
                var has_valid_product_lot = _.every(order.orderlines.models, function(line){
                    return line.has_valid_product_lot();
                });

                var lines = order.get_orderlines();
                var len = Math.min(lines.length);
                var j = 0;
                var qty = 0;
                for(var i=0; i<len; i++){
                    qty = qty + lines[i].quantity;
                }


                if(!has_valid_product_lot){
                    self.gui.show_popup('confirm',{
                        'title': _t('Empty Serial/Lot Number'),
                        'body':  _t('One or more product(s) required serial/lot number.'),
                        confirm: function(){
                            self.gui.show_screen('payment');
                        },
                    });
                }
                else if(len<=0){
//                    self.gui.back();
                    self.gui.show_popup('dialog', {
                        title: 'Warning',
                        body: "Empty Order",
                    });
                }
                else if(qty<=0){
                    self.gui.back();
                    self.gui.show_popup('dialog', {
                        title: 'Warning',
                        body: "Order Quantity Is Empty",
                    });
                }

                else{
                    if(client != null){
                        var order = self.pos.get_order();
                        var client = order.get_client().id;
                        var client_name = order.get_client().name;
                        var lines = order.get_orderlines();
                        var pos_orders = self.pos.get_order();
                        var bill = pos_orders.get_total_with_tax()
                        var order_id = self.pos.attributes.selectedOrder.name

                        rpc.query({
                            model: 'pos.payment_status',
                            method: 'payment_status',
                            args: [bill, order_id, client, client_name],
                            }).then(function (result){
                                if(result){
                                }
                            });

                            self.gui.show_screen('payment');
                    }
                    else{
                        self.gui.back();
//                        self.gui.show_popup('error',{
//                        'title': _t('Customer Not Selected'),
//                        'body':  _t('Please select a valid customer....'),
//                        });
                        self.gui.show_popup('dialog', {
                            title: 'Warning',
                            body: "Please select a valid customer",
                        });
                    }
                }
            });
            this.$('.set-customer').click(function(){
                self.gui.show_screen('clientlist');
            });
        }
    });

});
