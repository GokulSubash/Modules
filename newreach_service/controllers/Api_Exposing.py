from odoo.fields import Datetime
from odoo.http import request
from odoo import http
import json
from odoo import models, fields, api, _
import datetime
from datetime import datetime


class log_in_credentials(http.Controller):
    def userLogin(self, **kwargs):
        username = kwargs.get('username')
        password = kwargs.get('password')
        db = kwargs.get('db')
        uid = request.session.authenticate(db, username, password)
        if uid:
            jsondata = json.dumps(uid)
            return jsondata
        else:
            return False

    @http.route('/api/login', methods=['POST'], auth='public', csrf=False)
    def login(self, **kwargs):
        username = kwargs.get('username')
        password = kwargs.get('password')
        db = kwargs.get('db')
        uid = request.session.authenticate(db, username, password)

        data = {'username': username, 'password': password, 'uid': uid, 'resp': 1}
        data1 = {'resp': 0}
        val = json.dumps(data)
        val1 = json.dumps(data1)
        if uid:
            jsondata = json.dumps(uid)
            return val
        else:
            return val1

    @http.route('/newreach/country/details', methods=['GET'], auth='public', csrf=False)
    def get_country_details(self, **kwargs):

        countries = request.env['res.country'].search([])
        country = {'country': []}
        for i in countries:

            vals = {'name': i.name, 'id': i.id, 'states': []}
            for state in i.state_ids:
                vals['states'].append({'id': state.id, 'name': state.name})
            country['country'].append(vals)
        country = json.dumps(country)
        return country

    @http.route('/newreach/product/category', methods=['GET'], auth='public', csrf=False)
    def get_product_details(self, **kwargs):

        products = request.env['product.product'].sudo().search([])
        category = request.env['product.category'].sudo().search([])
        category_dict = {'category': []}
        for record in category:
            vals = {'name': record.name, 'id': record.id, 'products': []}
            for data in products:
                if data.categ_id.id == record.id:
                    send_image = data.image_medium
                    if send_image is not False:
                        send_image = send_image.decode("utf-8")
                    else:
                        send_image = False
                    vals['products'].append({'productId': data.id,
                                             'productName': data.name,
                                             'unitPrice': data.list_price,
                                             'internalReferance': data.default_code,
                                             'image': send_image
                                             })
            category_dict['category'].append(vals)
        category_dict = json.dumps(category_dict)
        return category_dict

    @http.route('/newreach/customer/create', methods=['POST'], auth='public', csrf=False)
    def customer_create(self, **kwargs):

        uid = self.userLogin(**kwargs)
        if uid:
            val = {
                'name': kwargs.get('name'),
                'email': kwargs.get('email'),
                'street': kwargs.get('street'),
                'street2': kwargs.get('street2'),
                'city': kwargs.get('city'),
                'zip': kwargs.get('zip'),
                'idNumber': kwargs.get('idNumber'),
                'idExpDate': kwargs.get('idExpDate'),
                'issuePlace': kwargs.get('issuePlace'),
                'dob': kwargs.get('dob'),
                'idtype': kwargs.get('idtype'),
                'firstname': kwargs.get('firstname'),
                'lastName': kwargs.get('lastName'),
                'image1': kwargs.get('image1'),
                'gen': kwargs.get('gen'),
                'customer_type': kwargs.get('customer_type'),
                'county_residence': kwargs.get('county_residence'),
                'medicalFirstName': kwargs.get('medicalFirstName'),
                'medicalLastName': kwargs.get('medicalLastName'),
                'medicalDob': kwargs.get('medicalDob'),
                'medicalidNumber': kwargs.get('medicalidNumber'),
                'medicalIdExpDate': kwargs.get('medicalIdExpDate'),
                'medicalCounty': kwargs.get('medicalCounty'),
                'medicalIssueName': kwargs.get('medicalIssueName'),
                'medicalIssueId': kwargs.get('medicalIssueId'),
                'medicalImage': kwargs.get('medicalImage'),
                'medicalCertificateImage': kwargs.get('medicalCertificateImage'),

            }
            user = request.env['res.partner'].sudo().create(val)
            return 'Ok'

    @http.route('/newreach/product', methods=['GET'], auth='public', csrf=False)
    def productListing(self, **kwargs):
        if kwargs.get('productId'):
            product = request.env['product.template'].sudo().search([('id', '=', int(kwargs.get('productId')))])
            vals = {
                'productId': product.id,
                'productName': product.name,
                'unitPrice': product.list_price,
                'internalReferance': product.default_code,
                'image': product.image_medium.decode("utf-8"),

            }
            productVals = json.dumps(vals)
            return productVals

        else:
            products = request.env['product.product'].sudo().search([])
            productsInfo = {'products': []}
            for product in products:

                send_image = product.image_medium
                if send_image is not False:
                    send_image = send_image.decode("utf-8")
                else:
                    send_image = False
                vals = {
                    'productId': product.id,
                    'productName': product.name,
                    'unitPrice': product.list_price,
                    'image': send_image,
                    'categ_id': product.categ_id.id,
                    'categ_name': product.categ_id.name,
                    'description': product.description_sale,
                }
                productsInfo['products'].append(vals)
            productVals = json.dumps(productsInfo)
            return productVals

    @http.route('/newreach/pos/order/create', methods=['POST'], auth='public', csrf=False)
    def onlineBookingPos(self, **kwargs):
        uid = self.userLogin(**kwargs)
        if uid:
            sessions = request.env['pos.session'].search(
                [('state', 'not in',
                  ('opening_control', 'closing_control', 'closed'))])
            for i in sessions:
                if '(' not in i.name:
                    session = i

            vals = {'session_id': session.id, 'date_order': fields.Datetime.now(), 'purchase_type': 'mobile_app',
                    'partner_id': int(uid), 'lines': [], 'name': request.env['ir.sequence'].get('pos.order')}

            line_vals = {
                'product_id': int(kwargs.get('product_id')),
                'qty': float(kwargs.get('qty')),
                'price_unit': float(kwargs.get('unitPrice')),
            }
            vals['lines'].append((0, 0, line_vals))
            request.env['pos.order'].sudo().create(vals)
            return "success"

    @http.route('/newreach/idtype', methods=['GET'], auth='public', csrf=False)
    def idtype(self, **kwargs):
        idTypes = request.env['new.reach.id'].sudo().search([])
        idVals = {'val': []}
        for idtype in idTypes:
            vals = {'id': idtype.id, 'name': idtype.name}
            idVals['val'].append(vals)
        productVals = json.dumps(idVals)
        return productVals

    @http.route('/newreach/order/create', methods=['POST'], auth='public', csrf=False, )
    def onlineBookingSlaeOrder(self, **kwargs):
        uid = self.userLogin(**kwargs)
        try:
            if uid:
                user = request.env['res.users'].sudo().search([('id', '=', int(uid))])
                sales_team = request.env['crm.team'].sudo().search([('name', '=', 'Mobile')])
                sales_channel = sales_team.id
                delivery_type = kwargs.get('delivery_type')
                vals = {
                    'partner_id': user.partner_id.id,
                    'picking_policy': 'one',
                    'team_id': sales_channel,
                    'delivery_type': delivery_type,
                    'delivery_status': 'not_delivered',
                    'purchase_type': 'mobile_app',
                    'order_line': []
                }

                lines = eval(kwargs.get('line'))
                partnerPurchaseVals = {'purchased': []}
                for i in lines:
                    maxQty = 0
                    buyedQty = 0
                    product = request.env['product.product'].sudo().search([('id', '=', int(i['product_id']))])
                    vals1 = {
                        'product_id': int(i['product_id']),
                        'product_uom_qty': float(i.get('qty')),
                        'price_unit': float(i.get('priceUnit'))
                    }

                    if product.categ_id.id:
                        if user.partner_id.customer_type == 'adult_customer':
                            maxQty = float(product.categ_id.maximumLimitAdult)
                        elif user.partner_id.customer_type == 'medical_customer':
                            maxQty = float(product.categ_id.maximumLimitMedical)
                        else:
                            return "You are not a Valid User/Id Expired please check Your ID or Contact Store "
                        purchase_lines = user.partner_id.mapped('purchased')
                        purchase_line_pr = purchase_lines.filtered(
                            lambda r: r.productCategType.id == product.categ_id.id)

                        if purchase_line_pr:
                            buyedQty = float(purchase_line_pr.qty)
                            afterOrderQty = buyedQty + float(i.get('qty'))
                            if maxQty >= afterOrderQty:
                                vals['order_line'].append((0, 0, vals1))
                                partnerPurchaseVals['purchased'].append((0, 0, {'productCategType': product.categ_id.id,
                                                                                'qty': afterOrderQty}))  # to add the quantity to partner form
                            else:
                                return "Your Daily Limit for {0} category is exceed".format(product.categ_id.name)

                        else:
                            buyedQty = 0.0
                            afterOrderQty = buyedQty + float(i.get('qty'))
                            if maxQty >= afterOrderQty:
                                vals['order_line'].append((0, 0, vals1))
                                partnerPurchaseVals['purchased'].append(
                                    (0, 0, {'productCategType': product.categ_id.id, 'qty': afterOrderQty}))
                            else:
                                return "Your Daily Limit for {0} category is exceed".format(product.categ_id.name)
                    else:
                        vals['order_line'].append((0, 0, vals1))
                for item in partnerPurchaseVals['purchased']:
                    purchase_lines = user.partner_id.mapped('purchased')
                    purchase_line_pr = purchase_lines.filtered(
                        lambda r: r.productCategType.id == item[2]['productCategType'])
                    if purchase_line_pr:
                        purchase_line_pr.qty = item[2]['qty']
                    else:
                        val = {'purchased': []}
                        val['purchased'].append(item)
                        user.partner_id.write(val)
                saleOrder = request.env['sale.order'].sudo().create(vals)
                valsPartnerForm = []
                return 'Order Successfully Placed'
        except:
            return "Something Went Wrong!.. Please try Again later "

    @http.route('/newreach/customer', methods=['POST'], auth='public', csrf=False)
    def employee_creation(self, **kwargs):
        uid = self.userLogin(**kwargs)
        if uid:
            user = request.env['res.users'].search([('id', '=', int(uid))])
            user_image = user.image
            if user_image is not False:
                user_image = user_image.decode('utf-8')
            else:
                user_image = False
            user_info = {'id': user.id, 'profile_name': user.name, 'email': user.email, 'username': user.login,
                         'phone': user.phone, 'country': user.country_id.name, 'image': user_image}
            jsondata = json.dumps(user_info)
            return jsondata
        else:
            return "Something Went Wrong!.. please try Again later "

    @http.route('/newreach/history', methods=['POST'], auth='public', csrf=False)
    def order_history(self, **kwargs):
        uid = self.userLogin(**kwargs)
        if uid:
            client = request.env['res.users'].sudo().search([('id', '=', uid)])
            partner_id = client.partner_id.id
            order_history = request.env['sale.order'].sudo().search([('partner_id', '=', partner_id)])

            history = {'history': []}
            for i in order_history:
                status = i.delivery_status
                delivery_status = 0
                if status == 'delivered':
                    delivery_status = '1'
                elif status == 'not_delivered':
                    delivery_status = '2'
                elif status == 'cancel':
                    delivery_status = '0'
                date = i.date_order
                date_string = str(date)
                date_order1 = datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S').date()

                date_order = str(date_order1)
                qr_code = str(i.qr_image)
                order_id = i.name
                vals = {
                    'order_id': order_id,
                    'date': date_order,
                    'total': i.amount_total,
                    'amount_tax': i.amount_tax,
                    'delivery_status': delivery_status,
                    'lines': [],
                    'qr_image': qr_code
                }
                for line in i.order_line:
                    vals['lines'].append({'product': line.product_id.name,
                                          'product_image': line.product_id.image_medium.decode("utf-8"),
                                          'qty': line.product_uom_qty,
                                          'unit_price': line.price_unit,
                                          'sub_total': line.price_subtotal
                                          })
                history['history'].append(vals)
            order_details = json.dumps(history)
            return order_details

    @http.route('/newreach/pending_payments', methods=['POST'], auth='public', csrf=False)
    def pending_payments(self, **kwargs):
        uid = self.userLogin(**kwargs)
        if uid:
            client = request.env['res.users'].sudo().search([('id', '=', uid)])
            partner_id = client.partner_id.id
            order_history = request.env['sale.order'].sudo().search([('partner_id', '=', partner_id),
                                                                     ('payment_status', '=', 'Not_Completed')])

            history = {'history': []}
            for i in order_history:
                status = i.delivery_status
                delivery_status = 0
                if status == 'delivered':
                    delivery_status = '1'
                elif status == 'not_delivered':
                    delivery_status = '2'
                elif status == 'cancel':
                    delivery_status = '0'
                date = i.date_order
                date_string = str(date)
                date_order1 = datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S').date()
                date_order = str(date_order1)
                qr_code = str(i.qr_image)
                order_id = i.name
                vals = {
                    'order_id': order_id,
                    'date': date_order,
                    'total': i.amount_total,
                    'delivery_status': delivery_status,
                    'lines': [],
                    'qr_image': qr_code
                }
                for line in i.order_line:
                    vals['lines'].append({'product': line.product_id.name,
                                          'product_image': line.product_id.image_medium.decode("utf-8"),
                                          'qty': line.product_uom_qty,
                                          'unit_price': line.price_unit,
                                          'sub_total': line.price_subtotal
                                          })
                history['history'].append(vals)
            order_details = json.dumps(history)
            return order_details
