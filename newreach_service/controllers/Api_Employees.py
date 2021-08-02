from odoo.http import request
from odoo import http
import json
import datetime
from datetime import datetime
import pusher
import requests
import base64

class newreach_employees(http.Controller):

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

    @http.route('/api/employeelogin', methods=['POST'], auth='public', csrf=False)
    def login(self, **kwargs):
        uid = self.userLogin(**kwargs)
        if uid:
            jsondata = json.dumps(uid)
            return "1"
        else:
            return "wrong credential"

    @http.route('/newreach/pickup', methods=['POST'], auth='public', csrf=False)
    def get_pickup_Details(self, **kwargs):
        uid = self.userLogin(**kwargs)
        if uid:
            pickup_pos = request.env['pos.order'].search([('delivery_type', '=', 'instore'),
                                                          ('product_status', '=', 1)])
            pickup_sales = request.env['sale.order'].search([('delivery_type', '=', 'instore'),
                                                             ('product_status', '=', 1)])
            picking = {'pickup': []}
            for i in pickup_pos:
                street = str(i.partner_id.street)
                street2 = str(i.partner_id.street2)
                city = str(i.partner_id.city)
                state_id = str(i.partner_id.state_id.name)
                zip_code = str(i.partner_id.zip)
                country_id = str(i.partner_id.country_id.name)
                address = street+', '+street2+', '+city+', '+state_id+', '+zip_code+', '+country_id
                mobile = i.partner_id.mobile

                date = i.date_order
                date_string = str(date)
                date_string2 = date_string[:19]
                date_order1 = datetime.strptime(date_string2, '%Y-%m-%d %H:%M:%S').date()
                date_order = str(date_order1)

                order = i.pos_reference
                order_id = order[6:]
                vals = {'order_id': order_id, 'customer': i.partner_id.name, 'address': address, 'mobile': mobile,
                        'date': date_order, 'amount_tax': i.amount_tax, 'total': i.amount_total,
                        'lines': []}
                for line in i.lines:
                    vals['lines'].append({'product': line.product_id.name,
                                          'qty': line.qty, 'unit_price': line.price_unit,
                                          'sub_total': line.price_subtotal_incl})
                picking['pickup'].append(vals)
            for i in pickup_sales:
                street = str(i.partner_id.street)
                street2 = str(i.partner_id.street2)
                city = str(i.partner_id.city)
                state_id = str(i.partner_id.state_id.name)
                zip_code = str(i.partner_id.zip)
                country_id = str(i.partner_id.country_id.name)
                address = street+', '+street2+', '+city+', '+state_id+', '+zip_code+', '+country_id
                mobile = i.partner_id.mobile

                date = i.date_order
                date_string = str(date)
                date_string2 = date_string[:19]
                date_order1 = datetime.strptime(date_string2, '%Y-%m-%d %H:%M:%S').date()
                date_order = str(date_order1)
                order = i.name

                vals = {'order_id': order, 'customer': i.partner_id.name, 'address': address, 'mobile': mobile,
                        'date': date_order, 'amount_tax': i.amount_tax, 'total': i.amount_total,
                        'lines': []}
                for line in i.order_line:
                    vals['lines'].append({'product': line.product_id.name,
                                          'qty': line.product_uom_qty, 'unit_price': line.price_unit,
                                          'sub_total': line.price_subtotal})
                picking['pickup'].append(vals)
            picking = json.dumps(picking)
            return picking

        else:
            return "Something Went Wrong!... please try Again later "

    @http.route('/newreach/delivery', methods=['POST'], auth='public', csrf=False)
    def delivery_Details(self, **kwargs):
        uid = self.userLogin(**kwargs)
        if uid:
            delivery_sales = request.env['sale.order'].search([('delivery_type', '=', 'home_delivery'),
                                                               ('product_status', '=', 1)])
            delivery_pos = request.env['pos.order'].search([('delivery_type', '=', 'home_delivery'),
                                                            ('product_status', '=', 1)])
            delivery_data = {'delivery': []}

            for i in delivery_pos:
                street = str(i.partner_id.street)
                street2 = str(i.partner_id.street2)
                city = str(i.partner_id.city)
                state_id = str(i.partner_id.state_id.name)
                zip_code = str(i.partner_id.zip)
                country_id = str(i.partner_id.country_id.name)
                address = street+', '+street2+', '+city+', '+state_id+', '+zip_code+', '+country_id
                mobile = i.partner_id.mobile

                date = i.date_order
                date_string = str(date)
                date_string2 = date_string[:19]
                date_order1 = datetime.strptime(date_string2, '%Y-%m-%d %H:%M:%S').date()
                date_order = str(date_order1)

                order = i.pos_reference
                order_id = order[6:]

                vals = {'order_id': order_id, 'customer': i.partner_id.name, 'address': address, 'mobile': mobile,
                        'date': date_order, 'amount_tax': i.amount_tax, 'total': i.amount_total,
                        'lines': []}
                for line in i.lines:
                    vals['lines'].append({'product': line.product_id.name,
                                          'qty': line.qty, 'unit_price': line.price_unit,
                                          'sub_total': line.price_subtotal_incl})
                delivery_data['delivery'].append(vals)
            for i in delivery_sales:
                street = str(i.partner_id.street)
                street2 = str(i.partner_id.street2)
                city = str(i.partner_id.city)
                state_id = str(i.partner_id.state_id.name)
                zip_code = str(i.partner_id.zip)
                country_id = str(i.partner_id.country_id.name)
                address = street+', '+street2+', '+city+', '+state_id+', '+zip_code+', '+country_id
                mobile = i.partner_id.mobile

                date = i.date_order
                date_string = str(date)
                date_string2 = date_string[:19]
                date_order1 = datetime.strptime(date_string2, '%Y-%m-%d %H:%M:%S').date()
                date_order = str(date_order1)

                order = i.name

                vals = {'order_id': order, 'customer': i.partner_id.name, 'address': address, 'mobile': mobile,
                        'date': date_order, 'amount_tax': i.amount_tax, 'total': i.amount_total,
                        'lines': []}

                for line in i.order_line:
                    vals['lines'].append({'product': line.product_id.name,
                                          'qty': line.product_uom_qty, 'unit_price': line.price_unit,
                                          'sub_total': line.price_subtotal})
                delivery_data['delivery'].append(vals)
            delivery_data = json.dumps(delivery_data)
            return delivery_data

        else:
            return "Something Went Wrong!.. please try Again later "

    @http.route('/newreach/pickupconfirm', methods=['POST'], auth='public', csrf=False)
    def get_pickup_confirm(self, **kwargs):
        order = kwargs.get('order_id')
        if 'SO' in order:
            order_id = order
            status = kwargs.get('status')
            val = {
                'order_id': order_id,
                'status': kwargs.get('status'),
            }

            record = request.env['sale.order'].search([('name', '=', order_id)])
            record.write({'delivery_status': status, 'product_status': '2'})

        else:
            order_id = 'Order '+order
            status = kwargs.get('status')
            val = {
                'order_id': order_id,
                'status': kwargs.get('status'),
            }
            record = request.env['pos.order'].search([('pos_reference', '=', order_id)])
            record.write({'delivery_status': status, 'product_status': '2'})

        return 'Pickup_Confirm'

    @http.route('/newreach/deliveryconfirm', methods=['POST'], auth='public', csrf=False)
    def get_delivery_Details(self, **kwargs):
        order = kwargs.get('order_id')
        if 'SO' in order:
            order_id = order
            sign = kwargs.get('sign')
            sign_data = sign[22:]
            status = kwargs.get('status')
            product_image = kwargs.get('product_image')
            val = {
                'order_id': order_id,
                'status': kwargs.get('status'),
                'sign': kwargs.get('sign'),
                'product_image': kwargs.get('product_image'),
            }
            record = request.env['sale.order'].search([('name', '=', order_id)])
            price = record.amount_total
            record.write({'delivery_status': status, 'product_status': '2', 'signature': sign_data,
                          'delivery_img': product_image})

            return 'Delivery_Confirm'
        else:
            order_id = 'Order '+order
            sign = kwargs.get('sign')
            sign_data = sign[22:]
            status = kwargs.get('status')
            product_image = kwargs.get('product_image')
            val = {
                'order_id': order_id,
                'status': kwargs.get('status'),
                'sign': kwargs.get('sign'),
                'product_image': kwargs.get('product_image'),
            }
            record = request.env['pos.order'].search([('pos_reference', '=', order_id)])
            record.write({'delivery_status': status, 'product_status': '2', 'signature': sign_data,
                          'delivery_img': product_image})

            return 'Delivery_Confirm'

    @http.route('/newreach/arterypay_list', methods=['POST'], auth='public', csrf=False)
    def get_arterypay_list(self, **kwargs):
        uid = self.userLogin(**kwargs)
        if uid:
            artery_pos = request.env['pos.order'].search(['|', ('payment_status', '=', 'Not_Completed'),
                                                          ('payment_status', '=', None)])
            artery_sales = request.env['sale.order'].search(['|', ('payment_status', '=', 'Not_Completed'),
                                                             ('payment_status', '=', None)])
            delivery_data = {'delivery': []}

            for i in artery_pos:
                street = str(i.partner_id.street)
                street2 = str(i.partner_id.street2)
                city = str(i.partner_id.city)
                state_id = str(i.partner_id.state_id.name)
                zip_code = str(i.partner_id.zip)
                country_id = str(i.partner_id.country_id.name)
                address = street+', '+street2+', '+city+', '+state_id+', '+zip_code+', '+country_id
                mobile = i.partner_id.mobile

                date = i.date_order
                date_string = str(date)
                date_string2 = date_string[:19]
                date_order1 = datetime.strptime(date_string2, '%Y-%m-%d %H:%M:%S').date()
                date_order = str(date_order1)
                order = i.pos_reference
                order_id = order[6:]
                artery_pay_qr = ''
                if i.artery_pay_QR:
                    artery_pay_qr = i.artery_pay_QR.decode("utf-8")
                else:
                    artery_pay_qr = None
                vals = {'order_id': order_id, 'customer': i.partner_id.name, 'address': address, 'mobile': mobile,
                        'date': date_order, 'amount_tax': i.amount_tax, 'total': i.amount_total, 'artery_pay_qr': artery_pay_qr,
                        'lines': []}
                for line in i.lines:
                    vals['lines'].append({'product': line.product_id.name,
                                          'qty': line.qty, 'unit_price': line.price_unit,
                                          'sub_total': line.price_subtotal_incl})
                delivery_data['delivery'].append(vals)
            for i in artery_sales:
                street = str(i.partner_id.street)
                street2 = str(i.partner_id.street2)
                city = str(i.partner_id.city)
                state_id = str(i.partner_id.state_id.name)
                zip_code = str(i.partner_id.zip)
                country_id = str(i.partner_id.country_id.name)
                address = street+', '+street2+', '+city+', '+state_id+', '+zip_code+', '+country_id
                mobile = i.partner_id.mobile

                date = i.date_order
                date_string = str(date)
                date_string2 = date_string[:19]
                date_order1 = datetime.strptime(date_string2, '%Y-%m-%d %H:%M:%S').date()
                date_order = str(date_order1)
                order = i.name
                if i.artery_pay_QR:
                    artery_pay_qr = i.artery_pay_QR.decode("utf-8")
                else:
                    artery_pay_qr = None
                vals = {'order_id': order, 'customer': i.partner_id.name, 'address': address, 'mobile': mobile,
                        'date': date_order, 'amount_tax': i.amount_tax, 'total': i.amount_total, 'artery_pay_qr': artery_pay_qr,
                        'lines': []}
                for line in i.order_line:
                    vals['lines'].append({'product': line.product_id.name,
                                          'qty': line.product_uom_qty, 'unit_price': line.price_unit,
                                          'sub_total': line.price_subtotal})
                delivery_data['delivery'].append(vals)
            delivery_data = json.dumps(delivery_data)
            return delivery_data

        else:
            return "Something Went Wrong!.. please try Again later "

    @http.route('/newreach/payment_scan', methods=['POST'], auth='public', csrf=False)
    def payment_scan(self, **kwargs):
        uid = self.userLogin(**kwargs)
        if uid:

            order_id = kwargs.get('order_id')
            pos_id = 'Order '+str(order_id)
            pos_orders = request.env['pos.order'].search([('pos_reference', '=', pos_id),
                                                          ('payment_status', '=', 'Not_Completed')])
            sale_orders = request.env['sale.order'].search([('name', '=', order_id),
                                                            ('payment_status', '=', 'Not_Completed')])

            data = {'data': []}
            if sale_orders:

                for i in sale_orders:
                    
                    date = i.date_order
                    date_string = str(date)
                    date_order1 = datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S').date()
                    date_order = str(date_order1)
                    qr_code = str(i.qr_image)
                    order_id = i.name
                    vals = {'order_id': order_id, 'customer': i.partner_id.name, 'date': date_order,
                            'amount_tax': i.amount_tax, 'total': i.amount_total, 'lines': [], 'qr_image': qr_code}
                    for line in i.order_line:
                        vals['lines'].append({'product': line.product_id.name,
                                              'qty': line.product_uom_qty, 'unit_price': line.price_unit,
                                              'sub_total': line.price_subtotal})
                    data['data'].append(vals)
                    order_details = json.dumps(data)
                    return order_details

            if pos_orders:


                for i in pos_orders:
                    date = i.date_order
                    date_string = str(date)
                    date_string2 = date_string[:19]
                    date_order1 = datetime.strptime(date_string2, '%Y-%m-%d %H:%M:%S').date()
                    date_order = str(date_order1)
                    order = i.pos_reference
                    order_id = order[6:]
                    vals = {'order_id': order_id, 'customer': i.partner_id.name,
                            'amount_tax': i.amount_tax, 'date': date_order, 'total': i.amount_total,
                            'lines': []}
                    for line in i.lines:
                        vals['lines'].append({'product': line.product_id.name,
                                              'qty': line.qty, 'unit_price': line.price_unit,
                                              'sub_total': line.price_subtotal_incl})
                    data['data'].append(vals)
                    order_details = json.dumps(data)
                    return order_details
            else:
                return "3"
        else:
            return 'Something went wrong'

    @http.route('/newreach/begin_transaction', methods=['POST'], auth='public', csrf=False)
    def begin_sale_transaction(self, **kwargs):
        order_id = kwargs.get('order_id')
        bill = kwargs.get('total')
        url = 'https://api.cashierautomation.com/api'

        credentials = request.env['test.connection'].search([])
        username = credentials.username
        password = credentials.password
        headers = {'Accept': "application/json", 'Content-Type': "application/json"}
        body = {"username": username, "password": password}
        data = json.dumps(body)
        api_endpoint = url+'/authorize/pos'
        authorize_response = requests.post(url=api_endpoint, data=data, headers=headers)

        if authorize_response.status_code == 200:
            details = json.loads(authorize_response.text)
            access_token = details["access_token"]
            refresh_token = details["refresh_token"]

            headers = {'accept': 'application/json', 'Authorization': 'Bearer %s' % access_token,
                       'Content-Type': 'application/json'}
            api_endpoint = url+'/device'
            device_response = requests.get(url=api_endpoint, headers=headers)
            device_response_data = json.loads(device_response.text)
            if device_response.status_code == 200:

                device_id = device_response_data["id"]
                is_device_ready = device_response_data["isReady"]
                is_dispense_enabled = device_response_data["isDispenseEnabled"]
                record_ids = request.env['test.connection'].search([])
                for record in record_ids:
                    record.write({
                        'device_id': device_id,
                    })


                headers = {'accept': 'application/json', 'Authorization': 'Bearer %s' % access_token,
                           'Content-Type': 'application/json'}
                api_endpoint = url+'/pusher/initialize-device'
                initialize_device_response = requests.post(url=api_endpoint, headers=headers)
                initialize_device_data = json.loads(initialize_device_response.text)
                if initialize_device_response.status_code == 200:
                    if is_dispense_enabled is True and is_device_ready is True:

                        channel_name = initialize_device_data["channelName"]
                        private_session_guid = initialize_device_data["privateSessionGuid"]

                        data = {
                            "deviceId": device_id,
                            "sessionId": private_session_guid,
                            "orderId": order_id,
                            "amount": bill,
                            "pinNumber": 0
                        }
                        vals = json.dumps(data)

                        headers = {'accept': 'application/json', 'Authorization': 'Bearer %s' % access_token,
                                   'Content-Type': 'application/json'}
                        api_endpoint = url+'/pusher/begin-sale-transaction'
                        begin_sale_transaction_device_response = requests.post(url=api_endpoint, headers=headers,
                                                                               data=vals)
                        if begin_sale_transaction_device_response.status_code == 200:
                            record_ids = request.env['test.connection'].search([('device_id', '=', device_id)])
                            for record in record_ids:
                                record.write({
                                    'access_token': access_token,
                                    'refresh_token': refresh_token,
                                    'session_id': private_session_guid,
                                    'channel_name': channel_name
                                })
                            trigger = "1"
                            return trigger
                        elif device_response.status_code == 400:
                            return
                        elif device_response.status_code == 401:
                            return
                        elif device_response.status_code == 500:
                            return

                    else:
                        trigger = "Device Not Ready"
                        return trigger

                elif device_response.status_code == 400:
                    return
                elif device_response.status_code == 401:
                    return
                elif device_response.status_code == 500:
                    return

            elif device_response.status_code == 400:
                return
            elif device_response.status_code == 401:
                return
            elif device_response.status_code == 500:
                return

        elif authorize_response.status_code == 400:
            return
        elif authorize_response.status_code == 401:
            return
        elif authorize_response.status_code == 500:
            return

    @http.route('/newreach/complete_transaction', methods=['POST'], auth='public', csrf=False)
    def complete_sale_transaction(self, **kwargs):

        order_id = kwargs.get('order_id')
        bill = kwargs.get('total')
        url = 'https://api.cashierautomation.com/api'

        credentials = request.env['test.connection'].search([])
        device_id = credentials.device_id
        session_id = credentials.session_id
        access_token = credentials.access_token
        headers = {'Accept': "application/json", 'Authorization': 'Bearer %s' % access_token,
                   'Content-Type': "application/json"}
        body = {
              "deviceId": device_id,
              "sessionId": session_id,
              "orderId": "",
              "amount": 0
            }
        data = json.dumps(body)
        api_endpoint = url+'/pusher/complete-transaction'
        complete_transaction = requests.post(url=api_endpoint, data=data, headers=headers)
        if complete_transaction.status_code == 200:
            trigger = "Transaction Completed"
            if 'SO' in order_id:
                record = request.env['sale.order'].search([('name', '=', order_id)])
                record.write({'payment_status': "Completed"})

            else:
                pos_id = 'Order ' + str(order_id)
                record = request.env['pos.order'].search([('pos_reference', '=', pos_id)])
                record.write({'payment_status': "Completed"})
            return trigger

        elif complete_transaction.status_code == 400:
            trigger = "Bad Request"
            return trigger

        elif complete_transaction.status_code == 401:
            trigger = "Unauthorized Request"
            return trigger

        elif complete_transaction.status_code == 500:
            trigger = "Internal Server Error"
            return trigger

        else:
            trigger = "Unknown Error.... Please Try Again Later"
            return trigger

    @http.route('/newreach/cancel_transaction', methods=['POST'], auth='public', csrf=False)
    def cancel_sale_transaction(self, **kwargs):
        order_id = kwargs.get('order_id')
        bill = kwargs.get('total')
        url = 'https://api.cashierautomation.com/api'

        credentials = request.env['test.connection'].search([])
        device_id = credentials.device_id
        session_id = credentials.session_id
        access_token = credentials.access_token
        headers = {'Accept': "application/json", 'Authorization': 'Bearer %s' % access_token,
                   'Content-Type': "application/json"}
        body = {
              "deviceId": device_id,
              "sessionId": session_id,
              "orderId": "",
              "amount": 0
            }
        data = json.dumps(body)
        api_endpoint = url+'/pusher/cancel-transaction'
        complete_transaction = requests.post(url=api_endpoint, data=data, headers=headers)

        if complete_transaction.status_code == 200:
            trigger = "Last Transaction Cancelled"
            return trigger
        elif complete_transaction.status_code == 400:
            trigger = "Bad Request"
            return trigger
        elif complete_transaction.status_code == 401:
            trigger = "Unauthorized"
            return trigger

        elif complete_transaction.status_code == 500:
            trigger = "Internal Server Error"
            return trigger

        else:
            return

    @http.route("/api/pusher/auth/", methods=['POST'], auth='public', csrf=False, cors='*')
    def pusher_authentication(self, socket_id, channel_name):

        pusher_client = pusher.Pusher(
            app_id='719815',
            key='c3a8cce24410c4f00d2c',
            secret='7ccb380d749b65d852be',
            cluster='ap2',
            ssl=True
        )

        auth = pusher_client.authenticate(
            channel=channel_name,
            socket_id=socket_id
        )
        return json.dumps(auth)
