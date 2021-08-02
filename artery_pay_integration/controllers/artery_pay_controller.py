from odoo import http
from odoo.http import request
import logging
import json

_logger = logging.getLogger(__name__)


class ArteryPayPaymentVerification(http.Controller):
    @http.route('/artery_pay/payment_verification', type='json', methods=['POST'],auth='public',csrf=False)
    def payment_verification(self, **kwargs):
        data = request.httprequest.data
        data_dict = json.loads(data.decode('utf-8'))
        op_type = data_dict['type']
        merchant_handle = data_dict['merchant_handle']
        total_cents = data_dict['total_cents']
        external_purchase_id = data_dict['external_purchase_id']
        vals = {



        }
        artery_pos = request.env['pos.order'].sudo().search(['&', ('name', '=', external_purchase_id),
                                                             ('payment_status', '=', 'Not_Completed')])
        artery_sale = request.env['sale.order'].sudo().search(['&', ('name', '=', external_purchase_id),
                                                               ('payment_status', '=', 'Not_Completed')])
        if artery_pos:
            return 200
        elif artery_sale:
            return 200
        else:
            return 0
    @http.route('/artery_pay/payment_notification', type='json', methods=['POST'], auth='public', csrf=False)
    def payment_notification(self, **kwargs):
        data = request.httprequest.data
        data_dict = json.loads(data.decode('utf-8'))
        op_type = data_dict['type']
        merchant_handle = data_dict['merchant_handle']
        total_cents = data_dict['total_cents']
        external_purchase_id = data_dict['external_purchase_id']
        status = data_dict['status']

        artery_pos = request.env['pos.order'].sudo().search([('name', '=', external_purchase_id),
                                                             ('payment_status', '=', 'Not_Completed')])
        artery_sale = request.env['sale.order'].search([('name', '=', external_purchase_id),
                                                        ('payment_status', '=', 'Not_Completed')])
        if artery_pos:
            if status == 'COMPLETED':
                artery_pos.write({'payment_status': "Completed"})
                return 200
        elif artery_sale:
            if status == 'COMPLETED':
                artery_sale.write({'payment_status': "Completed"})
                return 200
        else:
            return 0
